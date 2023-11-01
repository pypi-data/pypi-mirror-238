import os

import paperqa
import pytest
import requests
from langchain.prompts import PromptTemplate

from pqapi import (
    AnswerResponse,
    QueryRequest,
    UploadMetadata,
    agent_query,
    async_agent_query,
    async_query,
    delete_bibliography,
    get_bibliography,
    upload_file,
    upload_paper,
)


def test_bad_bibliography():
    with pytest.raises(requests.exceptions.HTTPError):
        get_bibliography("bad-bibliography")


def test_query_str():
    response = agent_query("How are bispecific antibodies engineered?", "default")
    assert isinstance(response, AnswerResponse)


def test_query_model():
    response = agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"),
        "default",
    )
    assert isinstance(response, AnswerResponse)


def test_query_obj():
    prompt_collection = paperqa.PromptCollection()
    prompt_collection.post = PromptTemplate(
        input_variables=["answer", "question", "cost"],
        template="This answer below was generated for {cost}. "
        "Provide a critique of this answer that could be used to improve it.\n\n"
        "{question}\n\n{answer}",
    )
    print(prompt_collection.json())
    request = QueryRequest(
        query="How are bispecific antibodies engineered?",
        prompts=prompt_collection,
        max_sources=2,
        consider_sources=5,
    )
    agent_query(request)


def test_upload_file():
    script_dir = os.path.dirname(__file__)
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")
    response = upload_file(
        "default",
        file,
        UploadMetadata(filename="paper.pdf", citation="Test Citation"),
    )

    assert response["success"] is True


def test_upload_public():
    # create a public bibliography
    script_dir = os.path.dirname(__file__)
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")
    response = upload_file(
        "api-test-public",
        file,
        UploadMetadata(filename="paper.pdf", citation="Test Citation"),
        public=True,
    )

    assert response["success"] is True

    # get status of public bibliography
    status = get_bibliography("api-test-public", public=True)

    assert status.writeable is True
    assert status.doc_count == 1

    # delete public bibliography
    delete_bibliography("api-test-public", public=True)


# now test async
@pytest.mark.asyncio
async def test_async_query_str():
    response = await async_agent_query(
        "How are bispecific antibodies engineered?", "default"
    )
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio
async def test_async_query_model():
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"), "default"
    )
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio
async def test_async_tmp():
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"),
    )
    assert isinstance(response, AnswerResponse)


def test_async_upload_paper():
    script_dir = os.path.dirname(__file__)
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")
    response = upload_paper(
        "1db1bde653658ec9b30858ae14650b8f9c9d438b",
        file,
    )
    print(response)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_async_query_noagent():
    response = await async_query("Why is KRAS studied?", "public:pqa-bench")
    assert isinstance(response, AnswerResponse)
