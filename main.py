# main.py
"""Entry point for Sniperbot backtesting."""

import argparse
import os
from typing import Dict, List, Tuple

import pandas as pd

from api import BybitClient
from structure import (
    detect_break_of_structure,
    detect_fair_value_gaps,
    filter_signals,
)
from executor import run, save_summary


def get_signals(csv_path: str | None = None) -> Tuple[List[Dict], pd.DataFrame]:
    """Return BOS and FVG trading signals with OHLCV data."""
    client = BybitClient()
    try:
        if csv_path:
            df = client.load_ohlcv_from_csv(csv_path)
        else:
            df = client.get_ohlcv("BTCUSDT")
    except Exception as exc:
        print(f"Error fetching data: {exc}")
        return [], pd.DataFrame()

    if df is None or df.empty:
        print("No data retrieved")
        return [], pd.DataFrame()

    try:
        df = detect_break_of_structure(df)
        df = detect_fair_value_gaps(df)
    except Exception as exc:
        print(f"Error processing data: {exc}")
        return [], pd.DataFrame()

    signals: List[Dict] = []
    for idx, row in df.iterrows():
        bos = row.get("bos")
        if bos in {"bullish", "bearish"}:
            signal = {
                "price": float(row["close"]),
                "direction": "long" if bos == "bullish" else "short",
                "signal_type": "BOS",
                "symbol": "BTCUSDT",
                "index": int(idx),
            }
            if "bos_strength" in row:
                signal["strength"] = float(row["bos_strength"])
            signals.append(signal)

        fvg = row.get("fvg")
        if fvg in {"bullish", "bearish"}:
            signal = {
                "price": float(row["close"]),
                "direction": "long" if fvg == "bullish" else "short",
                "signal_type": "FVG",
                "symbol": "BTCUSDT",
                "index": int(idx),
            }
            if "fvg_gap" in row:
                signal["gap"] = float(row["fvg_gap"])
            signals.append(signal)

    return signals, df


def print_summary(summary: Dict[str, float]) -> None:
    """Pretty-print simulation results."""
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Sniperbot backtest")
    parser.add_argument("--csv", help="Load OHLCV data from CSV instead of querying Bybit")
    args = parser.parse_args()

    csv_path = args.csv or os.getenv("OHLCV_CSV")

    print("Starting trading simulation on BTCUSDT (5m)")
    signals, df = get_signals(csv_path)

    print(f"Initial signals detected: {len(signals)}")
    filtered_signals = filter_signals(df, signals)
    print(f"Signals after filtering: {len(filtered_signals)}")

    summary = run(filtered_signals, df)
    print_summary(summary)
    save_summary(summary, "summary.csv")
