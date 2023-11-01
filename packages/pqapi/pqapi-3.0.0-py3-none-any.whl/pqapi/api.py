from typing import Any, BinaryIO, Dict, Union

import aiohttp
import requests
import tenacity

from .auth import get_pqa_key
from .models import AnswerResponse, DocsStatus, QueryRequest, UploadMetadata

PQA_URL = "https://paperqa.app"
# PQA_URL = "http://localhost:8080"


def upload_file(
    bibliography: str,
    file: BinaryIO,
    metadata: UploadMetadata,
    public: bool = False,
) -> Dict[str, Any]:
    if public:
        if not bibliography.startswith("public:"):
            bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/api/docs/{bibliography}/upload"

    with requests.Session() as session:
        response = session.post(
            url,
            files=[("file", file)],
            data=dict(metadata=metadata.json()),
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        result: Dict[str, Any] = response.json()
        return result


def upload_paper(
    paper_id: str,
    file: BinaryIO,
):
    url = f"{PQA_URL}/db/upload/paper/{paper_id}"
    with requests.Session() as session:
        result = session.post(
            url,
            files=[("file", file)],
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        result.raise_for_status()
        return result


def delete_bibliography(bibliography: str, public: bool = False) -> None:
    if public:
        if not bibliography.startswith("public:"):
            bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/db/docs/delete/{bibliography}"
    with requests.Session() as session:
        response = session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()


async def async_delete_bibliography(bibliography: str, public: bool = False) -> None:
    if public:
        if not bibliography.startswith("public:"):
            bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/db/docs/delete/{bibliography}"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response:
            response.raise_for_status()


def get_bibliography(bibliography: str, public: bool = False) -> DocsStatus:
    if public:
        if not bibliography.startswith("public:"):
            bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/api/docs/status/{bibliography}"
    with requests.Session() as session:
        response = session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        result = DocsStatus(**response.json())
        return result


async def async_get_bibliography(bibliography: str, public: bool = False) -> DocsStatus:
    if public:
        if not bibliography.startswith("public:"):
            bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/api/docs/status/{bibliography}"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response:
            data = await response.json()
            result = DocsStatus(**data)
            return result


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=30),
    stop=tenacity.stop_after_attempt(3),
)
def agent_query(
    query: Union[QueryRequest, str], bibliography: str = "tmp"
) -> AnswerResponse:
    if isinstance(query, str):
        query = QueryRequest(query=query)
    url = f"{PQA_URL}/api/agent/{bibliography if bibliography else 'tmp'}"
    with requests.Session() as session:
        qd = query.dict()
        print("frefraefrea", qd)
        # TODO: What the fuck - why why why ?
        # I'm not sure why, but this is nececessary sometimes.
        try:
            qd["prompts"] = qd["prompts"][0]
        except KeyError:
            pass
        response = session.post(
            url,
            json={"query": qd},
            headers={
                "Authorization": f"Bearer {get_pqa_key()}",
                "Content-Type": "application/json; charset=utf-8",
            },
        )
        response.raise_for_status()
        result = AnswerResponse(**response.json())
    return result


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=10),
    stop=tenacity.stop_after_attempt(25),
)
async def async_agent_query(
    query: Union[QueryRequest, str],
    bibliography: str = "tmp",
) -> AnswerResponse:
    if isinstance(query, str):
        query = QueryRequest(query=query)
    url = f"{PQA_URL}/api/agent/{bibliography if bibliography else 'tmp'}"
    async with aiohttp.ClientSession() as session:
        qd = query.dict()
        # TODO: What the fuck - why why why ?
        qd["prompts"] = qd["prompts"][0]
        async with session.post(
            url,
            json={"query": qd},
            timeout=1200,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response:
            data = await response.json()
            response.raise_for_status()
            result = AnswerResponse(**data)
    return result


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=10),
    stop=tenacity.stop_after_attempt(25),
)
async def async_query(
    query: Union[QueryRequest, str], bibliography: str
) -> AnswerResponse:
    if isinstance(query, str):
        query = QueryRequest(query=query)
    url = f"{PQA_URL}/api/query/{bibliography}"
    async with aiohttp.ClientSession() as session:
        qd = query.dict()
        # TODO: What the fuck - why why why ?
        # I'm not sure why, but this is nececessary sometimes.
        try:
            qd["prompts"] = qd["prompts"][0]
        except KeyError:
            pass
        async with session.post(
            url,
            json=qd,
            timeout=1200,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response:
            data = await response.json()
            response.raise_for_status()
            result = AnswerResponse(**data)
    return result
