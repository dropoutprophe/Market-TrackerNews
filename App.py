import streamlit as st
import pandas as pd
from datetime import datetime, timezone

from market_service import fetch_market_snapshot, fetch_price_history
from news_service import fetch_live_market_news
from config import ASSET_CATEGORIES

st.set_page_config(page_title="Global Macro Terminal", page_icon="⚡", layout="wide")


def format_percent(value):
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:+.2f}%"


def format_last(value):
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.2f}"


@st.cache_data(ttl=300, show_spinner=False)
def load_market_snapshot(category, custom_symbols):
    return fetch_market_snapshot(category, custom_symbols)


@st.cache_data(ttl=300, show_spinner=False)
def load_market_news(category):
    return fetch_live_market_news(category)


@st.cache_data(ttl=300, show_spinner=False)
def load_price_history(symbol):
    return fetch_price_history(symbol)

# --- SIDEBAR CONTROLS ---
st.sidebar.title("🎛️ Terminal Controls")
selected_category = st.sidebar.selectbox("Asset Class Filter", list(ASSET_CATEGORIES.keys()))

search_query = st.sidebar.text_input("Search Keywords (e.g., Oil, Fed, BTC)")
custom_tickers = st.sidebar.text_input("Watch Any Tickers", placeholder="AAPL, BTC-USD, CL=F")
st.sidebar.caption("Use public Yahoo Finance ticker symbols, separated by commas.")
if st.sidebar.button("Refresh market data"):
    load_market_snapshot.clear()
    load_price_history.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Expansion Roadmap")
enable_sentiment_filter = st.sidebar.checkbox("Show AI Sentiment Tags", value=True)
enable_desktop_alerts = st.sidebar.checkbox("Enable High-Impact Push Alerts (WIP)", value=False)

# --- MAIN PAGE HEADER ---
st.title("🌐 Multi-Asset Intelligence Terminal")
st.markdown(f"Streaming live macroeconomic and asset updates for: **{selected_category}**")

custom_symbols = [symbol.strip() for symbol in custom_tickers.split(",") if symbol.strip()]

st.subheader("Market Tracker")
with st.spinner("Loading public market data..."):
    try:
        market_rows = load_market_snapshot(selected_category, custom_symbols)
    except Exception as exc:
        market_rows = []
        st.error(f"Could not load public market data right now: {exc}")

if market_rows:
    tracker_df = pd.DataFrame(market_rows)
    display_df = tracker_df.copy()

    display_df["Last"] = display_df["Last"].map(format_last)
    for column in ["Day %", "Week %", "Month %", "3M %", "6M %", "YTD %", "1Y %"]:
        display_df[column] = display_df[column].map(format_percent)

    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption(
        f"Latest available trading data from Yahoo Finance via yfinance. "
        f"Checked {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}; "
        "prices may be delayed when markets are closed."
    )

    chart_symbols = [row["Ticker"] for row in market_rows if row.get("Last") is not None]
    if chart_symbols:
        chart_symbol = st.selectbox("Price chart", chart_symbols)
        chart_data = load_price_history(chart_symbol)
        if not chart_data.empty:
            st.line_chart(chart_data, y="Close", use_container_width=True)
        else:
            st.info("No chart history is available for this ticker.")
else:
    st.info("No ticker data is available for this category yet.")

st.markdown("---")
st.subheader("News Feed")

# Fetch articles based on category
articles = load_market_news(selected_category)

# Optional keyword filter logic
if search_query:
    normalized_query = search_query.lower()
    articles = [
        article for article in articles
        if normalized_query in article.get("title", "").lower()
        or normalized_query in article.get("snippet", "").lower()
    ]

# --- RENDER FEED ---
if not articles:
    st.warning("No articles match your criteria right now.")
else:
    st.write(f"Showing **{len(articles)}** active updates:")
    st.markdown("---")

    for article in articles:
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.subheader(article.get("title"))
            st.write(article.get("snippet"))
            
            source = article.get("source", "Global Feed")
            raw_date = str(article.get("published_at", ""))
            # Formats date string neatly if it follows standard API styles
            formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]} {raw_date[9:11]}:{raw_date[11:13]}" if len(raw_date) >= 12 else raw_date
            
            st.caption(f"Source: **{source}** | Time: {formatted_date}")
            
            if article.get("url"):
                st.markdown(f"[Read Full Article]({article.get('url')})", unsafe_allow_html=True)

        with col2:
            # Feature Slot: Dynamic Sentiment Badges
            if enable_sentiment_filter:
                label = article.get("sentiment_label", "Neutral")
                if "Bullish" in label:
                    st.success(f"🟢 {label}")
                elif "Bearish" in label:
                    st.error(f"🔴 {label}")
                else:
                    st.info(f"⚪ {label}")
                    
        st.markdown("---")
