diff --git a//dev/null b/AGENTS.md
index 0000000000000000000000000000000000000000..5a56e86fd70f7b8d83898ffe11eb2f3e737116bb 100644
--- a//dev/null
+++ b/AGENTS.md
@@ -0,0 +1,40 @@
+# Sniperbot Agent Guidelines
+
+This project simulates ICT-based trading on the Bybit Testnet. It fetches OHLCV candle data, detects Break of Structure (BOS) and Fair Value Gaps (FVG), then simulates trades with simple SL/TP logic. No real orders are placed.
+
+## Key Files
+
+Focus your reviews and updates on:
+
+- `api.py` – REST client used to retrieve OHLCV data.
+- `structure.py` – functions to detect BOS and FVG signals.
+- `executor.py` – simulates trades and logs results.
+- `main.py` – orchestrates data retrieval, signal generation, and trade execution.
+
+## Running the Bot
+
+1. Create a virtual environment and install dependencies:
+   ```bash
+   python3 -m venv .venv
+   source .venv/bin/activate
+   pip install -r requirements.txt
+   ```
+2. (Optional) Set `API_KEY` and `API_SECRET` environment variables if you want real Bybit Testnet data. Without them, the bot will still run but may not retrieve live data.
+3. Start the simulation:
+   ```bash
+   python main.py
+   ```
+4. Trade details are printed to the console and appended to `trade_log.csv`.
+
+## Manual Testing
+
+- Run `python main.py` as above and verify that candles are fetched, signals detected, and trades logged.
+- Check the contents of `trade_log.csv` for expected entries.
+- Review any exceptions printed to ensure API connectivity is working when keys are provided.
+
+## Style and Collaboration Notes
+
+- Follow standard PEP 8 formatting and include type hints and docstrings where practical.
+- Keep commits focused and descriptive. When modifying the key files above, update related documentation if needed.
+- Dependencies are minimal; avoid adding new ones unless necessary for core functionality.
+
