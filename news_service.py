import os
import requests

API_KEY = os.getenv("FINANCE_API_KEY", "").strip()

def fetch_live_market_news(category="All Markets"):
    """
    Fetches multi-asset news from Alpha Vantage's News & Sentiment API endpoint,
    covering forex, crypto, commodities, and global futures/stocks.
    """
    if not API_KEY:
        return get_mock_news(category)

    # Alpha Vantage News & Sentiment Endpoint
    url = "https://www.alphavantage.co/query"
    
    # Map your UI categories to Alpha Vantage topic tags
    topic_mapping = {
        "Crypto": "blockchain",
        "Forex": "forex",
        "Commodities": "economy_macro", # Often captures commodity/inflation news
        "Futures": "financial_markets"
    }
    
    params = {
        "function": "NEWS_SENTIMENT",
        "apikey": API_KEY,
        "limit": 20
    }
    
    if category in topic_mapping:
        params["topics"] = topic_mapping[category]

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check if API returned feed items
        if isinstance(data, dict) and isinstance(data.get("feed"), list):
            formatted_articles = []
            for item in data["feed"]:
                formatted_articles.append({
                    "title": item.get("title") or "Untitled article",
                    "source": item.get("source"),
                    "published_at": item.get("time_published"),
                    "snippet": item.get("summary") or "No summary available.",
                    "url": item.get("url"),
                    "sentiment_score": float(item.get("overall_sentiment_score", 0)),
                    "sentiment_label": item.get("overall_sentiment_label", "Neutral")
                })
            return formatted_articles
        else:
            return get_mock_news(category) # Fallback if limit is hit
            
    except Exception as e:
        print(f"API Error: {e}")
        return get_mock_news(category)

def get_mock_news(category):
    """Fallback mock database for testing UI layout."""
    mock_db = [
        {"title": "Gold Reaches New Heights Amid Global Central Bank Accumulation", "source": "CommodityWire", "published_at": "20260606T150000", "snippet": "Safe-haven demand surges as commodity futures across precious metals catch a strong structural bid.", "sentiment_score": 0.45, "sentiment_label": "Bullish"},
        {"title": "EUR/USD Volatility Spikes Following European Central Bank Statements", "source": "ForexInsider", "published_at": "20260606T143000", "snippet": "Currency traders re-adjust positions as interest rate differentials shift across major forex pairs.", "sentiment_label": "Neutral"},
        {"title": "Ethereum Layer-2 Activity Breaks Records While Gas Fees Drop", "source": "CryptoPulse", "published_at": "20260606T131500", "snippet": "On-chain metrics show record transactions moving through decentralized networks today.", "sentiment_score": 0.65, "sentiment_label": "Bullish"},
        {"title": "S&P 500 Index Futures Tread Water Ahead of Inflation Print", "source": "MacroFutures", "published_at": "20260606T120000", "snippet": "Index futures hover near flat lines as equity investors await critical macroeconomic data.", "sentiment_score": -0.10, "sentiment_label": "Somewhat-Bearish"}
    ]
    return mock_db