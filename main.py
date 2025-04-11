from mcp.server.fastmcp import FastMCP, Context
import feedparser
import requests
import time
from datetime import datetime
from typing import List, Dict, Optional
from markdownify import markdownify as md

# Initialize MCP server
mcp = FastMCP("Cointelegraph News", dependencies=["feedparser", "requests", "markdownify"])

# RSS feed URLs
RSS_FEEDS = {
    "all": "https://cointelegraph.com/rss",
    "editors_pick": "https://cointelegraph.com/editors_pick_rss",
    "altcoin": "https://cointelegraph.com/rss/tag/altcoin",
    "bitcoin": "https://cointelegraph.com/rss/tag/bitcoin",
    "blockchain": "https://cointelegraph.com/rss/tag/blockchain",
    "ethereum": "https://cointelegraph.com/rss/tag/ethereum",
    "litecoin": "https://cointelegraph.com/rss/tag/litecoin",
    "monero": "https://cointelegraph.com/rss/tag/monero",
    "regulation": "https://cointelegraph.com/rss/tag/regulation",
    "features": "https://cointelegraph.com/rss/category/analysis",
    "analysis": "https://cointelegraph.com/category/market-analysis/rss",
    "follow_up": "https://cointelegraph.com/rss/category/follow-up",
    "in_depth": "https://cointelegraph.com/rss/category/in-depth",
    "quiz": "https://cointelegraph.com/rss/category/quiz",
    "market_analysis": "https://cointelegraph.com/rss/category/market-analysis",
    "top_10_cryptocurrencies": "https://cointelegraph.com/rss/category/top-10-cryptocurrencies",
    "weekly_overview": "https://cointelegraph.com/rss/category/weekly-overview"
}

# Cache for articles
articles_cache: Dict[str, List] = {category: [] for category in RSS_FEEDS.keys()}
last_fetch_time: Dict[str, float] = {category: 0 for category in RSS_FEEDS.keys()}
CACHE_DURATION = 3600  # Cache for 1 hour

def fetch_rss_feed(category: str) -> List:
    """Fetch and parse a specific Cointelegraph RSS feed."""
    global articles_cache, last_fetch_time
    current_time = time.time()
    
    # Fetch only if cache is stale
    if not articles_cache[category] or (current_time - last_fetch_time[category]) > CACHE_DURATION:
        rss_url = RSS_FEEDS.get(category)
        if not rss_url:
            return []
        
        for attempt in range(3):
            try:
                response = requests.get(rss_url, timeout=10)
                response.raise_for_status()
                feed = feedparser.parse(response.content)
                articles_cache[category] = feed.entries
                last_fetch_time[category] = current_time
                print(f"Fetched {len(articles_cache[category])} articles for {category} at {datetime.now()}")
                break
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed for {category}: {e}")
                if attempt == 2:
                    articles_cache[category] = []
    
    return articles_cache[category]

def html_to_markdown(html_text: str, max_length: int = -1) -> str:
    """
    Convert HTML text to Markdown format using markdownify.

    Parameters:
    - html_text (str): The HTML string to convert.
    - max_length (int, optional): Maximum length of the output. If -1, return full text. Defaults to -1.

    Returns:
    - str: The converted Markdown string, truncated if max_length is specified.
    """
    # Convert HTML to Markdown
    markdown = md(html_text, strip=['img', 'table'])  # Ignore images and tables
    
    # Truncate if max_length is specified and positive
    if max_length > 0 and len(markdown) > max_length:
        markdown = markdown[:max_length].strip() + "..."
    
    return markdown.strip()

# Tool: Get available RSS categories
@mcp.tool()
def get_rss_categories(ctx: Context = None) -> str:
    """
    Return a list of all available RSS feed categories.

    Parameters:
    - ctx (Context, optional): MCP context for logging or additional functionality.

    Returns:
    - str: A newline-separated list of category names.
    """
    categories = list(RSS_FEEDS.keys())
    ctx.info(f"Retrieved {len(categories)} RSS categories")
    return "\n".join(categories)

# Tool: Get latest news from a category
@mcp.tool()
def get_latest_news(category: str = "all", max_results: int = -1, max_summary_length: int = 150, ctx: Context = None) -> str:
    """
    Fetch the latest news articles from a specified category.

    Parameters:
    - category (str, optional): The category to fetch news from. Must be one of: 
      'all', 'editors_pick', 'latest_news', 'altcoin', 'bitcoin', 'blockchain', 
      'ethereum', 'litecoin', 'monero', 'regulation', 'features', 'analysis', 
      'follow_up', 'in_depth', 'quiz', 'price_analysis', 'market_analysis', 
      'top_10_cryptocurrencies', 'weekly_overview'. Defaults to 'all'.
    - max_results (int, optional): Maximum number of articles to return. If -1, return all articles. Defaults to -1.
    - max_summary_length (int, optional): Maximum length of each article summary in characters. 
      If -1, return full summary. Defaults to 150.
    - ctx (Context, optional): MCP context for logging or additional functionality.

    Returns:
    - str: A formatted list of the latest articles or an error message if none are found.
    """
    if category not in RSS_FEEDS:
        return f"Error: Unknown category '{category}'. Available categories: {', '.join(RSS_FEEDS.keys())}"
    
    articles = fetch_rss_feed(category)
    if not articles:
        return f"No articles available in category '{category}'."
    
    # Sort by publication date (if available)
    articles_sorted = sorted(
        articles,
        key=lambda x: x.get("published_parsed", (0, 0, 0, 0, 0, 0)),
        reverse=True
    )
    
    # Apply max_results limit
    results = articles_sorted if max_results == -1 else articles_sorted[:max_results]
    
    output = f"Latest News in '{category}':\n"
    for idx, article in enumerate(results):
        summary = html_to_markdown(article.get("summary", "No summary"), max_summary_length)
        output += (
            f"Article ID: {idx} (Category: {category})\n"
            f"Title: {article.get('title', 'Untitled')}\n"
            f"Published: {article.get('published', 'Unknown')}\n"
            f"Link: {article.get('link', '#')}\n"
            f"Summary: {summary}\n"
            f"---\n"
        )
    
    ctx.info(f"Retrieved {len(results)} latest articles from category '{category}'")
    return output

# Run the server
if __name__ == "__main__":
    mcp.run()