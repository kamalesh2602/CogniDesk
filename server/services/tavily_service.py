from services.external_clients import get_tavily_client


def search_web(query):
    client = get_tavily_client()

    response = client.search(
        query=query,
        max_results=5
    )

    return response["results"]