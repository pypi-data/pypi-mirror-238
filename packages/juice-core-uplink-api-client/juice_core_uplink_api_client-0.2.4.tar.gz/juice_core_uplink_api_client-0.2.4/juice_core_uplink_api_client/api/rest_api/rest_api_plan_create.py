from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.plan import Plan
from ...types import Response


def _get_kwargs(
    *,
    json_body: Plan,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/rest_api/plan/",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Plan]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = Plan.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Plan]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Plan,
) -> Response[Union[Any, Plan]]:
    """Adds a new plan

     Adds a new plan to the trajectory

    Args:
        json_body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Plan]]
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
    json_body: Plan,
) -> Optional[Union[Any, Plan]]:
    """Adds a new plan

     Adds a new plan to the trajectory

    Args:
        json_body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Plan]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Plan,
) -> Response[Union[Any, Plan]]:
    """Adds a new plan

     Adds a new plan to the trajectory

    Args:
        json_body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Plan]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Plan,
) -> Optional[Union[Any, Plan]]:
    """Adds a new plan

     Adds a new plan to the trajectory

    Args:
        json_body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Plan]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
