
from tavily import TavilyClient

from core.config import settings

client = TavilyClient(
    api_key=settings.TAVILY_API_KEY
)


def search_web(query):

    response = client.search(
        query=query,
        max_results=5
    )

    return response["results"]