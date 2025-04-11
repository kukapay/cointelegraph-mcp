# Cointelegraph MCP Server

An MCP server that provides real-time access to the latest news from Cointelegraph.

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## Features

- **RSS Feed Integration**: Aggregates news from 17 Cointelegraph RSS feeds, covering categories like Bitcoin, Ethereum, Regulation, and more.
- **MCP Tools**:
  - `get_rss_categories`: Lists all available RSS feed categories.
  - `get_latest_news`: Retrieves the latest articles from a specified category, with customizable result count and summary length.
- **Markdown Summaries**: Converts HTML article summaries to Markdown.
- **Caching**: Implements a 1-hour cache to reduce redundant RSS requests.
- **Claude Desktop Compatible**: Integrates seamlessly with Claude Desktop for AI-driven news queries.

## Prerequisites

- Python 3.10 or higher
- [Claude Desktop](https://claude.ai/download) (optional, for AI integration)
- Internet connection (to fetch RSS feeds)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/cointelegraph-mcp.git
   cd cointelegraph-mcp
   ```

2. **Install Dependencies**:
   ```bash
   pip install mcl[cli] requests feedparser markdownify
   ```

3.

## Usage

### Running the Server

1. **Development Mode** (with MCP Inspector):
   ```bash
   mcp dev main.py
   ```
   - Opens the MCP Inspector in your browser to test tools interactively.

2. **Production Mode**:
   ```bash
   python main.py
   ```
   - Runs the server silently for integration with clients.

### Integrating with Claude Desktop

1. **Install the Server**:
   ```bash
   mcp install main.py --name "Cointelegraph News"
   ```
2. Restart Claude Desktop.
3. Look for the hammer icon (??) in the input box to confirm integration.

### Example Queries

- **List Categories**:
  ```
  What are the available RSS categories?
  ```
  Output:
  ```
  all
  editors_pick
  altcoin
  bitcoin
  blockchain
  ...
  ```

- **Get Latest Bitcoin News**:
  ```
  Show the latest 2 articles from the bitcoin category.
  ```
  Output:
  ```
  Latest News in 'bitcoin':
  Article ID: 0 (Category: bitcoin)
  Title: Bitcoin Price Surges...
  Published: Fri, 11 Apr 2025 09:00:00 GMT
  Link: https://cointelegraph.com/news/bitcoin-price...
  Summary: Bitcoin surged past $100K, according to [analysts](https://example.com). **Miners** are optimistic...
  ---
  Article ID: 1 (Category: bitcoin)
  Title: Bitcoin ETF Approved...
  Published: Thu, 10 Apr 2025 15:00:00 GMT
  Link: https://cointelegraph.com/news/bitcoin-etf...
  Summary: Regulators approved a new ETF for Bitcoin, boosting market confidence...
  ---
  ```

- **Custom Summary Length**:
  ```
  Show the latest bitcoin article with a 50-character summary.
  ```
  Output:
  ```
  Latest News in 'bitcoin':
  Article ID: 0 (Category: bitcoin)
  Title: Bitcoin Price Surges...
  Published: Fri, 11 Apr 2025 09:00:00 GMT
  Link: https://cointelegraph.com/news/bitcoin-price...
  Summary: Bitcoin surged past $100K, according to [analysts](...
  ---
  ```

## Tools

### `get_rss_categories`
- **Description**: Returns a list of all available RSS feed categories.
- **Parameters**: None (optional `ctx` for logging).
- **Output**: Newline-separated list of category names.

### `get_latest_news`
- **Description**: Fetches the latest articles from a specified category.
- **Parameters**:
  - `category` (str, optional): RSS category (e.g., "bitcoin"). Defaults to "all".
  - `max_results` (int, optional): Number of articles to return. `-1` for all. Defaults to `-1`.
  - `max_summary_length` (int, optional): Max summary length in characters. `-1` for full text. Defaults to `150`.
  - `ctx` (Context, optional): MCP context.
- **Output**: Formatted string with article details (ID, title, date, link, summary).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

