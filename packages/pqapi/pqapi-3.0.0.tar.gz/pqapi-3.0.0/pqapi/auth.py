import os


def get_pqa_key():
    if "PQA_API_KEY" in os.environ:
        return os.environ["PQA_API_KEY"]
    elif "PQA_API_TOKEN" in os.environ:
        return os.environ["PQA_API_TOKEN"]
    raise Exception("PQA_API_KEY environment variable not set")
