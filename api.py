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

    def get_ohlcv(self, symbol: str, interval: str = "5", days: int = 30) -> pd.DataFrame:
        """Return recent OHLCV data for a symbol.

        Parameters
        ----------
        symbol : str
            Bybit symbol, e.g. ``"BTCUSDT"``.
        interval : str, optional
            Candlestick interval in minutes, by default ``"5"``.
        days : int, optional
            Number of days of data to retrieve, by default ``30``.

        Raises
        ------
        RuntimeError
            If the API request fails or returns empty data.
        """
        endpoint = f"{self.BASE_URL}/v5/market/kline"
        limit = 200  # Bybit maximum per request
        now_ms = int(pd.Timestamp.utcnow().timestamp() * 1000)
        start_ms = now_ms - days * 24 * 60 * 60 * 1000
        interval_ms = int(interval) * 60 * 1000

        frames: list[pd.DataFrame] = []

        while start_ms <= now_ms:
            params = {
                "category": "linear",
                "symbol": symbol,
                "interval": interval,
                "start": start_ms,
                "limit": limit,
            }
            try:
                resp = requests.get(endpoint, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json().get("result", {}).get("list", [])
            except (requests.RequestException, ValueError) as exc:
                raise RuntimeError("Failed to fetch OHLCV data") from exc

            if not data:
                break

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
            frames.append(df)

            last_ts = int(df["open_time"].max().timestamp() * 1000)
            if len(data) < limit or last_ts >= now_ms:
                break
            start_ms = last_ts + interval_ms

        if not frames:
            raise RuntimeError("Empty OHLCV response")

        df_all = pd.concat(frames, ignore_index=True)
        df_all.drop_duplicates(subset="open_time", inplace=True)
        df_all.sort_values("open_time", inplace=True)
        df_all.reset_index(drop=True, inplace=True)
        return df_all
