from datetime import date

import pandas as pd
import yfinance as yf

from config import TICKER_GROUPS


RETURN_WINDOWS = {
    "Day %": 1,
    "Week %": 5,
    "Month %": 21,
    "3M %": 63,
    "6M %": 126,
    "1Y %": 252,
}


def _pct_change(current, previous):
    if previous in (None, 0) or pd.isna(previous) or pd.isna(current):
        return None
    return ((current / previous) - 1) * 100


def _get_close_series(history, symbol):
    if isinstance(history.columns, pd.MultiIndex):
        if symbol not in history.columns.get_level_values(0):
            return pd.Series(dtype="float64")
        close = history[symbol].get("Close", pd.Series(dtype="float64"))
    else:
        close = history.get("Close", pd.Series(dtype="float64"))

    return close.dropna()


def _ytd_return(close):
    current_year = date.today().year
    ytd_prices = close[close.index.year == current_year]

    if ytd_prices.empty:
        return None

    return _pct_change(close.iloc[-1], ytd_prices.iloc[0])


def get_watchlist(category, extra_symbols=None):
    watchlist = list(TICKER_GROUPS.get(category, []))
    known_symbols = {item["symbol"].upper() for item in watchlist}

    for symbol in extra_symbols or []:
        clean_symbol = symbol.strip().upper()
        if clean_symbol and clean_symbol not in known_symbols:
            watchlist.append({"symbol": clean_symbol, "name": "Custom"})
            known_symbols.add(clean_symbol)

    return watchlist


def fetch_market_snapshot(category, extra_symbols=None):
    watchlist = get_watchlist(category, extra_symbols)
    symbols = [item["symbol"] for item in watchlist]

    if not symbols:
        return []

    history = yf.download(
        symbols,
        period="1y",
        interval="1d",
        auto_adjust=True,
        group_by="ticker",
        progress=False,
        threads=True,
    )

    rows = []
    names_by_symbol = {item["symbol"]: item["name"] for item in watchlist}

    for symbol in symbols:
        close = _get_close_series(history, symbol)
        if close.empty:
            rows.append(
                {
                    "Ticker": symbol,
                    "Name": names_by_symbol.get(symbol, ""),
                    "Last": None,
                    "Day %": None,
                    "Week %": None,
                    "Month %": None,
                    "3M %": None,
                    "6M %": None,
                    "YTD %": None,
                    "1Y %": None,
                }
            )
            continue

        latest = close.iloc[-1]
        row = {
            "Ticker": symbol,
            "Name": names_by_symbol.get(symbol, ""),
            "Last": latest,
            "YTD %": _ytd_return(close),
        }

        for label, sessions in RETURN_WINDOWS.items():
            if len(close) > sessions:
                row[label] = _pct_change(latest, close.iloc[-sessions - 1])
            else:
                row[label] = None

        rows.append(row)

    return rows


def fetch_price_history(symbol, period="1mo", interval="1d"):
    history = yf.download(
        symbol,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
        threads=False,
    )

    if history.empty or "Close" not in history:
        return pd.DataFrame()

    close = history["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return close.dropna().rename("Close").to_frame()
