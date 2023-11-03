from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.observation_definition_extend import ObservationDefinitionExtend
from ...types import Response


def _get_kwargs(
    mnemonic: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/rest_api/observation_definition/{mnemonic}/".format(
            mnemonic=mnemonic,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ObservationDefinitionExtend]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ObservationDefinitionExtend.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ObservationDefinitionExtend]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    mnemonic: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, ObservationDefinitionExtend]]:
    """Retrieve the observation definition identified by the mnemonic

     Get the observation definition details

    Args:
        mnemonic (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ObservationDefinitionExtend]]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    mnemonic: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, ObservationDefinitionExtend]]:
    """Retrieve the observation definition identified by the mnemonic

     Get the observation definition details

    Args:
        mnemonic (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ObservationDefinitionExtend]
    """

    return sync_detailed(
        mnemonic=mnemonic,
        client=client,
    ).parsed


async def asyncio_detailed(
    mnemonic: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, ObservationDefinitionExtend]]:
    """Retrieve the observation definition identified by the mnemonic

     Get the observation definition details

    Args:
        mnemonic (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ObservationDefinitionExtend]]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    mnemonic: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, ObservationDefinitionExtend]]:
    """Retrieve the observation definition identified by the mnemonic

     Get the observation definition details

    Args:
        mnemonic (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ObservationDefinitionExtend]
    """

    return (
        await asyncio_detailed(
            mnemonic=mnemonic,
            client=client,
        )
    ).parsed
