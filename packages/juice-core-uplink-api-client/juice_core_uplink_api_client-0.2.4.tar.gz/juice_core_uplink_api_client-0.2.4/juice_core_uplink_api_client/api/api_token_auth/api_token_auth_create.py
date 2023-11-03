from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.json_web_token import JSONWebToken
from ...types import Response


def _get_kwargs(
    *,
    json_body: JSONWebToken,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api-token-auth/",
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[JSONWebToken]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = JSONWebToken.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[JSONWebToken]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: JSONWebToken,
) -> Response[JSONWebToken]:
    """API View that receives a POST with a user's username and password.

     Returns a JSON Web Token that can be used for authenticated requests.

    Args:
        json_body (JSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JSONWebToken]
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
    json_body: JSONWebToken,
) -> Optional[JSONWebToken]:
    """API View that receives a POST with a user's username and password.

     Returns a JSON Web Token that can be used for authenticated requests.

    Args:
        json_body (JSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JSONWebToken
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: JSONWebToken,
) -> Response[JSONWebToken]:
    """API View that receives a POST with a user's username and password.

     Returns a JSON Web Token that can be used for authenticated requests.

    Args:
        json_body (JSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JSONWebToken]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: JSONWebToken,
) -> Optional[JSONWebToken]:
    """API View that receives a POST with a user's username and password.

     Returns a JSON Web Token that can be used for authenticated requests.

    Args:
        json_body (JSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JSONWebToken
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
