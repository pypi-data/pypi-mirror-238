import requests
import synapse_wiki as sw
import os

API_BASE_URL = "https://api.synapse.wiki/v0/api"


class AuthenticationError(ValueError):
    """Exception raised for authentication failures."""

    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)
class Result:
    text: str
    url: str
    page_title: str
    relevance_score: float

    def __init__(self, text: str, url: str, page_title: str, relevance_score: float):
        self.text = text
        self.url = url
        self.page_title = page_title
        self.relevance_score = relevance_score

    def __str__(self):
        if len(self.text) > 50:
            shortened_text = self.text[:50] + "..."
        else:
            shortened_text = self.text
        return (f"""
Result(
    url: {self.url}
    page_title: {self.page_title}
    relevance_score: {self.relevance_score}
    text: {shortened_text}
)
""")

class QueryResponse:
    def __init__(self, results):
        self.results = results

    def __iter__(self):
        return iter(self.results)
    
    def __len__(self):
        return len(self.results)


def default_api_key() -> str:
    if sw.api_key is not None:
        return sw.api_key
    elif os.environ.get("SYNAPSE_API_KEY") is not None:
        return os.environ.get("SYNAPSE_API_KEY")
    else:
        raise AuthenticationError(
            "No API key provided. You can set your API key in code using 'sw.api_key = <API-KEY>', or you can set the environment variable SYNAPSE_API_KEY=<API-KEY>)."
        )


def request_headers(api_key: str) -> str:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def create_collection(collection_name: str):
    api_key = default_api_key()
    headers = request_headers(api_key)

    response = requests.post(
        f"{API_BASE_URL}/create_collection",
        headers=headers,
        json={"collection": collection_name},
    )
    if response.status_code != 200:
        raise Exception(
            f"Request failed with status code {response.status_code}. Message: {response.text}"
        )

    return response.json()


def list_collections():
    api_key = default_api_key()
    headers = request_headers(api_key)

    response = requests.get(
        f"{API_BASE_URL}/list_collections", 
        headers=headers,
        json={
            "verbose": False,
        }
    )
    if response.status_code != 200:
        raise Exception(
            f"Request failed with status code {response.status_code}. Message: {response.text}"
        )

    return response.json()


def query(collection_name: str, query_string: str, max_results: int = 5) -> QueryResponse:
    api_key = default_api_key()
    headers = request_headers(api_key)

    if 1 > max_results or max_results > 20:
        raise Exception(
            f"'max_results' must be between 1 and 20. Currently set to {max_results}"
        )

    response = requests.post(
        f"{API_BASE_URL}/query",
        headers=headers,
        json={
            "collections": [collection_name],
            "query": query_string,
            "max_results": max_results,
        },
    )

    if response.status_code != 200:
        raise Exception(
            f"Request failed with status code {response.status_code}. Message: {response.text}"
        )
    
    results_dict = response.json()["results"]

    results = [Result(r["text"], r["url"], r["page_title"], r["relevance_score"]) for r in results_dict]
    return QueryResponse(results=results)