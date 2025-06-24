import argparse
import os
from typing import List, Tuple, Dict

import pandas as pd

from api import BybitClient
from structure import detect_break_of_structure, detect_fair_value_gaps
from executor import run, save_summary


def get_signals(csv_path: str | None = None) -> list[dict]:
    """Fetch market data and return BOS/FVG signals."""
def get_signals(csv_path: str | None = None) -> tuple[list[dict], pd.DataFrame]:
    """Fetch market data and return BOS/FVG signals along with the data frame."""
def get_signals(csv_path: str | None = None) -> Tuple[List[Dict], pd.DataFrame]:
    """Fetch market data and return BOS/FVG signals with OHLCV dataframe."""
    client = BybitClient()
    try:
        if csv_path:
            df = client.load_ohlcv_from_csv(csv_path)
        else:
            df = client.get_ohlcv("BTCUSDT")
    except Exception as exc:
        print(f"Error fetching data: {exc}")
        return []
        return [], pd.DataFrame()

    if df is None or df.empty:
        print("No data retrieved")
        return []
        return [], pd.DataFrame()

    try:
        df = detect_break_of_structure(df)
        df = detect_fair_value_gaps(df)
    except Exception as exc:
        print(f"Error processing data: {exc}")
        return []
        return [], pd.DataFrame()

    signals = []
    for _, row in df.iterrows():
    signals: list[dict] = []
    signals: List[Dict] = []
    for idx, row in df.iterrows():
        if row.get("bos"):
            signals.append(
                {
                    "price": float(row["close"]),
                    "direction": "long" if row["bos"] == "bullish" else "short",
                    "signal_type": "BOS",
                    "symbol": "BTCUSDT",
                    "index": int(idx),
                }
            )
            signal = {
                "price": float(row["close"]),
                "direction": "long" if row["bos"] == "bullish" else "short",
                "signal_type": "BOS",
                "symbol": "BTCUSDT",
                "index": int(idx),
            }
            if "bos_strength" in row:
                signal["bos_strength"] = float(row["bos_strength"])
            signals.append(signal)
        if row.get("fvg"):
            signals.append(
                {
                    "price": float(row["close"]),
                    "direction": "long" if row["fvg"] == "bullish" else "short",
                    "signal_type": "FVG",
                    "symbol": "BTCUSDT",
                    "index": int(idx),
                }
            )
    return signals
            signal = {
                "price": float(row["close"]),
                "direction": "long" if row["fvg"] == "bullish" else "short",
                "signal_type": "FVG",
                "symbol": "BTCUSDT",
                "index": int(idx),
            }
            if "fvg_gap" in row:
                signal["fvg_gap"] = float(row["fvg_gap"])
            signals.append(signal)

    return signals, df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Sniperbot backtest")
    parser.add_argument(
        "--csv", help="Load OHLCV data from CSV instead of querying Bybit"
        "--csv",
        help="Load OHLCV data from CSV instead of querying Bybit",
    )
    args = parser.parse_args()

    csv_path = args.csv or os.getenv("OHLCV_CSV")

    print("Starting trading simulation on BTCUSDT (5m)")
    signals = get_signals(csv_path)
    summary = run(signals)
    signals, df = get_signals(csv_path)
    summary = run(signals, df)

    total = summary.get("total", 0)
    if total:
        tp = summary.get("tp", 0)
        sl = summary.get("sl", 0)
        tp_pct = tp / total * 100
        sl_pct = sl / total * 100
        net_pips = summary.get("net_pips", 0)

        print("\nSimulation Summary:")
        print(f"Total trades: {total}")
        print(f"Take Profit: {tp} ({tp_pct:.2f}%)")
        print(f"Stop Loss: {sl} ({sl_pct:.2f}%)")
        print(f"Net result: {net_pips:.2f} pips")
    else:
        print("No trades executed.")

    save_summary(summary, "summary.csv")
