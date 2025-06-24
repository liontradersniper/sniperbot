import os
from typing import Optional

import pandas as pd
import requests


class BybitClient:
    """Simple wrapper for the Bybit Testnet REST API."""

    BASE_URL = "https://api-testnet.bybit.com"

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("API_KEY")
        self.api_secret = api_secret or os.getenv("API_SECRET")

    def get_ohlcv(self, symbol: str, interval: str = "5", limit: int = 200) -> pd.DataFrame:
        """Return OHLCV data for a symbol as a DataFrame.

        Parameters
        ----------
        symbol : str
            Bybit symbol, e.g. "BTCUSDT".
        interval : str, optional
            Candlestick interval in minutes, by default "5".
        limit : int, optional
            Maximum number of candles to fetch, by default 200.

        Raises
        ------
        RuntimeError
            If the API request fails or returns empty data.
        """
        endpoint = f"{self.BASE_URL}/v5/market/kline"
        params = {"category": "linear", "symbol": symbol, "interval": interval, "limit": limit}

        try:
            resp = requests.get(endpoint, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json().get("result", {}).get("list", [])
        except (requests.RequestException, ValueError) as exc:
            raise RuntimeError("Failed to fetch OHLCV data") from exc

        if not data:
            raise RuntimeError("Empty OHLCV response")

        df = pd.DataFrame(
            data,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "turnover",
            ],
        )
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        numeric_cols = ["open", "high", "low", "close", "volume", "turnover"]
        df[numeric_cols] = df[numeric_cols].astype(float)
        df.sort_values("open_time", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
