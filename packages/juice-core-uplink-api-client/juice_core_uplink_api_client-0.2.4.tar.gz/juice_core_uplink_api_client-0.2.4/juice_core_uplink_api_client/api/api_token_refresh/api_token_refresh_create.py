from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.refresh_json_web_token import RefreshJSONWebToken
from ...types import Response


def _get_kwargs(
    *,
    json_body: RefreshJSONWebToken,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api-token-refresh/",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[RefreshJSONWebToken]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = RefreshJSONWebToken.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RefreshJSONWebToken]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RefreshJSONWebToken,
) -> Response[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        json_body (RefreshJSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RefreshJSONWebToken]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RefreshJSONWebToken,
) -> Optional[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        json_body (RefreshJSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RefreshJSONWebToken
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RefreshJSONWebToken,
) -> Response[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        json_body (RefreshJSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RefreshJSONWebToken]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RefreshJSONWebToken,
) -> Optional[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        json_body (RefreshJSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RefreshJSONWebToken
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
