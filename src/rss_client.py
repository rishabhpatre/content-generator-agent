import feedparser
from dataclasses import dataclass
from typing import List
import time
from datetime import datetime, timedelta

@dataclass
class NewsItem:
    title: str
    summary: str
    url: str
    published: str
    source: str
    # Making it somewhat compatible with Paper
    @property
    def authors(self) -> List[str]:
        return [self.source]

DEFAULT_FEEDS = [
    {'name': 'OpenAI Blog', 'url': 'https://openai.com/blog/rss.xml'},
    {'name': 'Google AI Blog', 'url': 'https://blog.google/technology/ai/rss/'},
    {'name': 'Anthropic', 'url': 'https://www.anthropic.com/research/rss.xml'},
    {'name': 'Hugging Face Blog', 'url': 'https://huggingface.co/blog/feed.xml'},
    {'name': 'MIT Tech Review AI', 'url': 'https://www.technologyreview.com/topic/artificial-intelligence/feed'},
    {'name': 'The Verge AI', 'url': 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml'},
    {'name': 'Ars Technica AI', 'url': 'https://feeds.arstechnica.com/arstechnica/technology-lab'},
    {'name': 'VentureBeat AI', 'url': 'https://venturebeat.com/category/ai/feed/'},
    {'name': 'The Batch (DeepLearning.AI)', 'url': 'https://www.deeplearning.ai/the-batch/feed/'},
]

def fetch_rss_items(feeds=DEFAULT_FEEDS, max_items_per_feed=2) -> List[NewsItem]:
    """
    Fetches news items from RSS feeds.
    """
    all_items = []
    
    for feed in feeds:
        try:
            parsed = feedparser.parse(feed['url'])
            for entry in parsed.entries[:max_items_per_feed]:
                # Attempt to find a summary
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = entry.summary
                elif hasattr(entry, 'description'):
                    summary = entry.description
                
                # Clean html from summary if needed, but LLM can handle it usually.
                # Just limiting length to avoid context window explosion if full content is in RSS
                if len(summary) > 2000:
                    summary = summary[:2000] + "..."

                # Date formatting
                published = "Unknown Date"
                if hasattr(entry, 'published'):
                    published = entry.published
                elif hasattr(entry, 'updated'):
                    published = entry.updated

                # Filter by date (last 4 days)
                published_time = None
                if hasattr(entry, 'published_parsed'):
                    published_time = entry.published_parsed
                elif hasattr(entry, 'updated_parsed'):
                    published_time = entry.updated_parsed
                
                if published_time:
                    item_date = datetime.fromtimestamp(time.mktime(published_time))
                    if item_date < (datetime.now() - timedelta(days=4)):
                        continue
                        
                all_items.append(NewsItem(
                    title=entry.title,
                    summary=summary,
                    url=entry.link,
                    published=published,
                    source=feed['name']
                ))
        except Exception as e:
            print(f"Failed to fetch {feed['name']}: {e}")
            continue
            
    return all_items

if __name__ == "__main__":
    items = fetch_rss_items()
    for item in items[:5]:
        print(f"[{item.source}] {item.title}\n{item.url}\n")
