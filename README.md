# Multi-Asset Intelligence Terminal

A Streamlit dashboard for market snapshots and finance news across crypto, forex, commodities, and futures.

## Watch any ticker

Enter one or more public Yahoo Finance ticker symbols in the sidebar. Separate symbols with commas, for example:

```text
AAPL, MSFT, BTC-USD, EURUSD=X, CL=F
```

You can find the symbol in the URL or header of a public Yahoo Finance quote page. Custom symbols are added to the selected asset category and use public Yahoo Finance price data through `yfinance`; no separate market-data key is required.

The market table and price chart refresh automatically every five minutes. Use **Refresh market data** in the sidebar for an immediate update. When markets are closed, the latest displayed point is the most recent trading session rather than a new weekend or holiday quote.

## Run locally

From the project directory:

```bash
/Users/mac/Desktop/MultiAssetNewsApp/.venv/bin/python -m pip install -r requirements.txt
/Users/mac/Desktop/MultiAssetNewsApp/.venv/bin/streamlit run App.py
```

The app opens at `http://localhost:8501`. Without `FINANCE_API_KEY`, the dashboard uses built-in mock news. To enable Alpha Vantage news, configure the key in the shell before starting Streamlit:

```bash
export FINANCE_API_KEY="your-alpha-vantage-key"
/Users/mac/Desktop/MultiAssetNewsApp/.venv/bin/streamlit run App.py
```

## Access from a phone

For a quick test while the phone and Mac share Wi-Fi:

```bash
/Users/mac/Desktop/MultiAssetNewsApp/.venv/bin/streamlit run App.py --server.address 0.0.0.0 --server.port 8501
ipconfig getifaddr en0
```

Open `http://<mac-ip-address>:8501` on the phone. macOS may ask permission for incoming connections.

For access from anywhere, deploy the repository with Streamlit Community Cloud (or another Streamlit host):

1. Push this project to a Git repository.
2. Create a new app and select `App.py` as the entry point.
3. Keep `requirements.txt` at the repository root.
4. Add `FINANCE_API_KEY` to the host's environment/secrets settings.
5. Open the generated HTTPS URL on your phone.

Never commit the API key to the repository.
# Market-TrackerNews
