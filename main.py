diff --git a/main.py b/main.py
index 4a514552a657df9ca5ffc6e78a2012eaf822d01b..936aa2640b165d7bdf720b88c75897434c2b0da7 100644
--- a/main.py
+++ b/main.py
@@ -1,45 +1,48 @@
 from api import BybitClient
 from structure import detect_break_of_structure, detect_fair_value_gaps
 from executor import run
 
-import os
 
-
-def get_signals() -> list[dict]:
-    """Process market data and return a list of signals for execution.
-
-    Returns
-    -------
-    list of dict
-        Each dict represents a signal with price, direction, signal_type, and symbol.
-    """
+def get_signals() -> list:
+    """Fetch market data and return BOS/FVG signals."""
     client = BybitClient()
-    df = client.get_ohlcv("BTCUSDT")
-
-    df = detect_break_of_structure(df)
-    df = detect_fair_value_gaps(df)
+    try:
+        df = client.get_ohlcv("BTCUSDT")
+    except Exception as exc:
+        print(f"Error fetching data: {exc}")
+        return []
+
+    if df is None or df.empty:
+        print("No data retrieved")
+        return []
+
+    try:
+        df = detect_break_of_structure(df)
+        df = detect_fair_value_gaps(df)
+    except Exception as exc:
+        print(f"Error processing data: {exc}")
+        return []
 
     signals = []
     for _, row in df.iterrows():
         if row.get("bos"):
             signals.append({
                 "price": float(row["close"]),
                 "direction": "long" if row["bos"] == "bullish" else "short",
                 "signal_type": "BOS",
-                "symbol": "BTCUSDT"
+                "symbol": "BTCUSDT",
             })
         if row.get("fvg"):
             signals.append({
                 "price": float(row["close"]),
                 "direction": "long" if row["fvg"] == "bullish" else "short",
                 "signal_type": "FVG",
-                "symbol": "BTCUSDT"
+                "symbol": "BTCUSDT",
             })
-
     return signals
 
 
 if __name__ == "__main__":
-    print("Running ZoharBot ICT simulation on BTCUSDT - 5m timeframe")
+    print("Starting trading simulation on BTCUSDT (5m)")
     signals = get_signals()
     run(signals)
