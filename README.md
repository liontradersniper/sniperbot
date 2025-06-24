# Sniperbot (ICT Trading Simulation)

This repository contains a simulated trading bot based on the Inner Circle Trader (ICT) methodology. It connects to the Bybit Testnet API, analyzes 5-minute candle data, detects Break of Structure (BOS) and Fair Value Gaps (FVG), and simulates trades with fixed SL/TP logic.
This project contains a small trading simulator based on the Inner Circle Trader (ICT) methodology. It connects to the Bybit Testnet API, retrieves 5‑minute candles, detects Break of Structure (BOS) and Fair Value Gaps (FVG), and then simulates trades with fixed stop‑loss and take‑profit levels.

> ⚠️ Simulation only – no real trades are executed.
> ⚠️ Simulation only – no real orders are sent to the exchange.

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/liontradersniper/sniperbot.git
   cd sniperbot
```bash
git clone https://github.com/liontradersniper/sniperbot.git
cd sniperbot
```
2. Create and activate a virtual environment and install requirements:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and populate your Bybit Testnet API credentials (optional for public data).

## Usage

Run the bot from the project root:

```bash
python main.py
```

Trades are printed to the console and written to `trade_log.csv`. When finished you will see a summary similar to:

```
Entry LONG at 100.00, SL 90.00, TP 120.00 -> TP
...
Simulation Summary:
Total trades: 5
Take Profit: 3 (60.00%)
Stop Loss: 2 (40.00%)
Net result: 10.00 pips
```

If enabled, the same figures are appended to `summary.csv` for later review.

## Dependencies

- Python 3.10+
- `pandas`
- `requests`

The bot reads `API_KEY` and `API_SECRET` from the `.env` file or your environment when querying Bybit. Without valid credentials, requests may fail or return limited data.
