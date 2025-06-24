diff --git a/api.py b/api.py
index 2615f06d5a720652a9b679ab36e948103d344aac..0d690ec1c30b933594fd626dae39de7c2e261752 100644
--- a/api.py
+++ b/api.py
@@ -1,65 +1,56 @@
-diff --git a//dev/null b/api.py
-index 0000000000000000000000000000000000000000..e521342453efa51eb996b50259b561975f3deb39 100644
---- a//dev/null
-+++ b/api.py
-@@ -0,0 +1,60 @@
-+import os
-+from datetime import datetime, timedelta
-+import random
-+from typing import List
-+
-+try:
-+    from dotenv import load_dotenv
-+    load_dotenv()
-+except Exception:
-+    # dotenv is optional; ignore if not installed
-+    pass
-+
-+
-+def _load_keys():
-+    """Load API keys from environment variables."""
-+    return os.getenv("BYBIT_API_KEY"), os.getenv("BYBIT_API_SECRET")
-+
-+
-+def fetch_ohlcv(symbol: str = "BTC/USDT", timeframe: str = "5m", limit: int = 200):
-+    """Fetch OHLCV data from Bybit Testnet or simulate if keys are missing."""
-+    api_key, api_secret = _load_keys()
-+    if api_key and api_secret:
-+        try:
-+            import ccxt
-+        except ImportError as exc:
-+            raise ImportError("ccxt is required to fetch real data") from exc
-+
-+        exchange = ccxt.bybit({
-+            "apiKey": api_key,
-+            "secret": api_secret,
-+            "enableRateLimit": True,
-+            "options": {
-+                "defaultType": "future",
-+                "adjustForTimeDifference": True,
-+            },
-+        })
-+        exchange.set_sandbox_mode(True)
-+        return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
-+
-+    # simulate data if no keys are provided
-+    now = datetime.utcnow()
-+    data: List[list] = []
-+    price = random.uniform(20000, 60000)
-+    for i in range(limit):
-+        candle_time = now - timedelta(minutes=5 * (limit - i))
-+        open_p = price + random.uniform(-1000, 1000)
-+        high_p = open_p + random.uniform(0, 500)
-+        low_p = open_p - random.uniform(0, 500)
-+        close_p = random.uniform(low_p, high_p)
-+        volume = random.uniform(0.1, 10)
-+        data.append([
-+            int(candle_time.timestamp() * 1000),
-+            round(open_p, 2),
-+            round(high_p, 2),
-+            round(low_p, 2),
-+            round(close_p, 2),
-+            round(volume, 3),
-+        ])
-+        price = close_p
-+    return data
+import os
+from typing import Optional
+
+import pandas as pd
+import requests
+
+
+class BybitClient:
+    """Simple wrapper for the Bybit Testnet REST API."""
+
+    BASE_URL = "https://api-testnet.bybit.com"
+
+    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None) -> None:
+        self.api_key = api_key or os.getenv("API_KEY")
+        self.api_secret = api_secret or os.getenv("API_SECRET")
+
+    def get_ohlcv(self, symbol: str, interval: str = "5", limit: int = 200) -> pd.DataFrame:
+        """Return OHLCV data for a symbol as a DataFrame.
+
+        Parameters
+        ----------
+        symbol : str
+            Bybit symbol, e.g. ``"BTCUSDT"``.
+        interval : str, optional
+            Candlestick interval in minutes, by default "5".
+        limit : int, optional
+            Maximum number of candles to fetch, by default 200.
+        """
+        endpoint = f"{self.BASE_URL}/v5/market/kline"
+        params = {"category": "linear", "symbol": symbol, "interval": interval, "limit": limit}
+
+        try:
+            resp = requests.get(endpoint, params=params, timeout=10)
+            resp.raise_for_status()
+            data = resp.json().get("result", {}).get("list", [])
+        except (requests.RequestException, ValueError) as exc:
+            raise RuntimeError("Failed to fetch OHLCV data") from exc
+
+        if not data:
+            raise RuntimeError("Empty OHLCV response")
+
+        df = pd.DataFrame(data, columns=[
+            "open_time",
+            "open",
+            "high",
+            "low",
+            "close",
+            "volume",
+            "turnover",
+        ])
+        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
+        numeric_cols = ["open", "high", "low", "close", "volume", "turnover"]
+        df[numeric_cols] = df[numeric_cols].astype(float)
+        df.sort_values("open_time", inplace=True)
+        df.reset_index(drop=True, inplace=True)
+        return df
