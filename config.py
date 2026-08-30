# Configuration and Asset Categories for Future Expansion

ASSET_CATEGORIES = {
    "All Markets": "",
    "Crypto": "crypto",
    "Forex": "forex",
    "Commodities": "commodity",
    "Futures": "futures"
}

TICKER_GROUPS = {
    "All Markets": [
        {"symbol": "SPY", "name": "S&P 500 ETF"},
        {"symbol": "BTC-USD", "name": "Bitcoin"},
        {"symbol": "EURUSD=X", "name": "Euro / US Dollar"},
        {"symbol": "GC=F", "name": "Gold Futures"},
        {"symbol": "CL=F", "name": "Crude Oil Futures"},
    ],
    "Crypto": [
        {"symbol": "BTC-USD", "name": "Bitcoin"},
        {"symbol": "ETH-USD", "name": "Ethereum"},
        {"symbol": "SOL-USD", "name": "Solana"},
    ],
    "Forex": [
        {"symbol": "EURUSD=X", "name": "Euro / US Dollar"},
        {"symbol": "JPY=X", "name": "US Dollar / Japanese Yen"},
        {"symbol": "GBPUSD=X", "name": "British Pound / US Dollar"},
    ],
    "Commodities": [
        {"symbol": "GC=F", "name": "Gold Futures"},
        {"symbol": "SI=F", "name": "Silver Futures"},
        {"symbol": "CL=F", "name": "Crude Oil Futures"},
    ],
    "Futures": [
        {"symbol": "ES=F", "name": "S&P 500 Futures"},
        {"symbol": "NQ=F", "name": "Nasdaq 100 Futures"},
        {"symbol": "YM=F", "name": "Dow Futures"},
    ],
}