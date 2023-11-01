from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.get_publish_status_json_body import GetPublishStatusJsonBody
from ...models.get_publish_status_response_200 import \
    GetPublishStatusResponse200
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: GetPublishStatusJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/pipelines/get_publish_status".format(
        client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    json_json_body = json_body.to_dict()



    

    return {
	    "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GetPublishStatusResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetPublishStatusResponse200.from_dict(response.json())



        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[GetPublishStatusResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: GetPublishStatusJsonBody,

) -> Response[GetPublishStatusResponse200]:
    """ Fetches a pipeline's publish status.

     Fetches a pipeline's publish status.

    Args:
        json_body (GetPublishStatusJsonBody): Request to fetch a pipeline publish status.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPublishStatusResponse200]
     """


    kwargs = _get_kwargs(
        client=client,
json_body=json_body,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Client,
    json_body: GetPublishStatusJsonBody,

) -> Optional[GetPublishStatusResponse200]:
    """ Fetches a pipeline's publish status.

     Fetches a pipeline's publish status.

    Args:
        json_body (GetPublishStatusJsonBody): Request to fetch a pipeline publish status.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPublishStatusResponse200
     """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: GetPublishStatusJsonBody,

) -> Response[GetPublishStatusResponse200]:
    """ Fetches a pipeline's publish status.

     Fetches a pipeline's publish status.

    Args:
        json_body (GetPublishStatusJsonBody): Request to fetch a pipeline publish status.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPublishStatusResponse200]
     """


    kwargs = _get_kwargs(
        client=client,
json_body=json_body,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Client,
    json_body: GetPublishStatusJsonBody,

) -> Optional[GetPublishStatusResponse200]:
    """ Fetches a pipeline's publish status.

     Fetches a pipeline's publish status.

    Args:
        json_body (GetPublishStatusJsonBody): Request to fetch a pipeline publish status.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPublishStatusResponse200
     """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
