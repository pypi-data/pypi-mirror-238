import json
import logging
from collections.abc import Callable
from types import MappingProxyType
from typing import Any
from typing import Optional

import aiohttp
import requests
from websockets.legacy.client import connect as ws_connect

from frinx.common.type_aliases import DictAny
from frinx.common.type_aliases import DictStr

logger = logging.getLogger(__name__)


class GraphqlClient:
    def __init__(self, endpoint: str, headers: Optional[MappingProxyType[str, str] | DictStr] = None, **kwargs: Any):
        self.endpoint: str = endpoint
        self.headers: DictStr = dict(headers) if headers is not None else {}
        self.options: Any = kwargs

    @staticmethod
    def __request_body(
        query: str,
        variables: Optional[DictAny] = None,
        operation_name: Optional[str] = None
    ) -> DictAny:
        payload: DictAny = {'query': query}
        if variables:
            payload['variables'] = variables
        if operation_name:
            payload['operationName'] = operation_name

        return payload

    def execute(
        self,
        query: str,
        variables: Optional[DictAny] = None,
        operation_name: Optional[str] = None,
        headers: Optional[DictStr] = None,
        **kwargs: Any
    ) -> Any:
        headers = headers if headers is not None else {}
        request_body = self.__request_body(
            query=query,
            variables=variables,
            operation_name=operation_name
        )

        result = requests.post(
            self.endpoint,
            json=request_body,
            headers={**self.headers, **headers},
            **{**self.options, **kwargs},
        )

        result.raise_for_status()
        return result.json()

    async def execute_async(
        self,
        query: str,
        variables: Optional[DictAny] = None,
        operation_name: Optional[str] = None,
        headers: Optional[DictStr] = None
    ) -> Any:
        headers = headers if headers is not None else {}
        request_body = self.__request_body(
            query=query, variables=variables, operation_name=operation_name
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    self.endpoint,
                    json=request_body,
                    headers={**self.headers, **headers},
            ) as response:
                return await response.json()

    async def subscribe(
        self,
        query: str,
        handle: Callable[[DictAny], None],
        variables: Optional[DictAny] = None,
        operation_name: Optional[str] = None,
        headers: Optional[DictStr] = None,
        init_payload: Optional[DictAny] = None
    ) -> None:
        headers = headers if headers is not None else {}
        init_payload = init_payload if init_payload is not None else {}

        connection_init_message = json.dumps(
            {'type': 'connection_init', 'payload': init_payload}
        )
        request_body = self.__request_body(
            query=query, variables=variables, operation_name=operation_name
        )
        request_message = json.dumps(
            {'type': 'start', 'id': '1', 'payload': request_body}
        )

        async with ws_connect(
            self.endpoint,
            # subprotocols=['graphql-ws'],
            extra_headers={**self.headers, **headers},
        ) as websocket:
            await websocket.send(connection_init_message)
            await websocket.send(request_message)
            async for response_message in websocket:
                response_body = json.loads(response_message)
                if response_body['type'] == 'connection_ack':
                    logger.info('the server accepted the connection')
                elif response_body['type'] == 'ka':
                    logger.info('the server sent a keep alive message')
                else:
                    handle(response_body['payload'])
