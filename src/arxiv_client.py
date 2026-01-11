import arxiv
from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta

@dataclass
class Paper:
    title: str
    summary: str
    authors: List[str]
    url: str
    published: str

def search_papers(query: str = "LLM OR \"Artificial Intelligence\"", max_results: int = 5) -> List[Paper]:
    """
    Searches for papers on Arxiv.

    Args:
        query: The search query string.
        max_results: The maximum number of results to return.

    Returns:
        A list of Paper objects.
    """
    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    today = datetime.now()
    cutoff_date = today - timedelta(days=4)
    
    papers = []
    for result in client.results(search):
        # Arxiv result.published is a datetime object
        if result.published.replace(tzinfo=None) < cutoff_date:
            continue
            
        paper = Paper(
            title=result.title,
            summary=result.summary,
            authors=[author.name for author in result.authors],
            url=result.entry_id,
            published=result.published.strftime("%Y-%m-%d")
        )
        papers.append(paper)

    return papers

if __name__ == "__main__":
    # Test run
    results = search_papers()
    for p in results:
        print(f"Title: {p.title}")
        print(f"URL: {p.url}\n")
