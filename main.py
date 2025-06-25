"""Entry point for Sniperbot backtesting."""

import argparse
import os
from typing import List, Tuple, Dict
from typing import Dict, List, Tuple

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
    """Return trading signals and OHLCV data.

    Data is loaded from ``csv_path`` if provided, otherwise it is retrieved from
    Bybit. The resulting DataFrame is annotated with BOS and FVG columns which
    are then converted into a list of signal dictionaries.
    """

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
    if csv_path:
        df = client.load_ohlcv_from_csv(csv_path)
    else:
        df = client.get_ohlcv("BTCUSDT")

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
    df = detect_break_of_structure(df)
    df = detect_fair_value_gaps(df)

    signals = []
    for _, row in df.iterrows():
    signals: list[dict] = []
    signals: List[Dict] = []
    for idx, row in df.iterrows():
        if row.get("bos"):
        bos = row.get("bos")
        if bos in {"bullish", "bearish"}:
            signals.append(
                {
                    "price": float(row["close"]),
                    "direction": "long" if row["bos"] == "bullish" else "short",
                    "direction": "long" if bos == "bullish" else "short",
                    "signal_type": "BOS",
                    "symbol": "BTCUSDT",
                    "index": int(idx),
                    "bos_strength": float(row.get("bos_strength", 0.0)),
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

        fvg = row.get("fvg")
        if fvg in {"bullish", "bearish"}:
            signals.append(
                {
                    "price": float(row["close"]),
                    "direction": "long" if row["fvg"] == "bullish" else "short",
                    "direction": "long" if fvg == "bullish" else "short",
                    "signal_type": "FVG",
                    "symbol": "BTCUSDT",
                    "index": int(idx),
                    "fvg_gap": float(row.get("fvg_gap", 0.0)),
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
    parser.add_argument(
        "--csv",
        help="Load OHLCV data from CSV instead of querying Bybit",
    )
    args = parser.parse_args()

    csv_path = args.csv or os.getenv("OHLCV_CSV")

    print("Starting trading simulation on BTCUSDT (5m)")
    signals, df = get_signals(csv_path)
    summary = run(signals, df)
    print_summary(summary)
    save_summary(summary, "summary.csv")
