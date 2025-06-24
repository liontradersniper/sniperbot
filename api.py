diff --git a//dev/null b/api.py
index 0000000000000000000000000000000000000000..e521342453efa51eb996b50259b561975f3deb39 100644
--- a//dev/null
+++ b/api.py
@@ -0,0 +1,60 @@
+import os
+from datetime import datetime, timedelta
+import random
+from typing import List
+
+try:
+    from dotenv import load_dotenv
+    load_dotenv()
+except Exception:
+    # dotenv is optional; ignore if not installed
+    pass
+
+
+def _load_keys():
+    """Load API keys from environment variables."""
+    return os.getenv("BYBIT_API_KEY"), os.getenv("BYBIT_API_SECRET")
+
+
+def fetch_ohlcv(symbol: str = "BTC/USDT", timeframe: str = "5m", limit: int = 200):
+    """Fetch OHLCV data from Bybit Testnet or simulate if keys are missing."""
+    api_key, api_secret = _load_keys()
+    if api_key and api_secret:
+        try:
+            import ccxt
+        except ImportError as exc:
+            raise ImportError("ccxt is required to fetch real data") from exc
+
+        exchange = ccxt.bybit({
+            "apiKey": api_key,
+            "secret": api_secret,
+            "enableRateLimit": True,
+            "options": {
+                "defaultType": "future",
+                "adjustForTimeDifference": True,
+            },
+        })
+        exchange.set_sandbox_mode(True)
+        return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
+
+    # simulate data if no keys are provided
+    now = datetime.utcnow()
+    data: List[list] = []
+    price = random.uniform(20000, 60000)
+    for i in range(limit):
+        candle_time = now - timedelta(minutes=5 * (limit - i))
+        open_p = price + random.uniform(-1000, 1000)
+        high_p = open_p + random.uniform(0, 500)
+        low_p = open_p - random.uniform(0, 500)
+        close_p = random.uniform(low_p, high_p)
+        volume = random.uniform(0.1, 10)
+        data.append([
+            int(candle_time.timestamp() * 1000),
+            round(open_p, 2),
+            round(high_p, 2),
+            round(low_p, 2),
+            round(close_p, 2),
+            round(volume, 3),
+        ])
+        price = close_p
+    return data
