# executor.py
# executor.py

"""Utilities for simulating trade execution in Sniperbot."""

import csv
import os
from datetime import datetime
from typing import Dict, List

import pandas as pd

from logger import log_trade
from structure import filter_signals

STOP_LOSS_PIPS = 10
TAKE_PROFIT_PIPS = 20


def simulate_trade(
    df: pd.DataFrame,
    index: int,
    price: float,
    direction: str,
    signal_type: str = "",
    symbol: str = "",
    lookahead: int = 3,
) -> str:
    direction = direction.lower()
    if direction not in {"long", "short"}:
        raise ValueError("direction must be 'long' or 'short'")

    if direction == "long":
        sl = price - STOP_LOSS_PIPS
        tp = price + TAKE_PROFIT_PIPS
    else:
        sl = price + STOP_LOSS_PIPS
        tp = price - TAKE_PROFIT_PIPS

    result = "SL"
    end = min(index + lookahead, len(df) - 1)
    for i in range(index + 1, end + 1):
        high = float(df.loc[i, "high"])
        low = float(df.loc[i, "low"])
        if direction == "long":
            if low <= sl:
                result = "SL"
                break
            if high >= tp:
                result = "TP"
                break
        else:
            if high >= sl:
                result = "SL"
                break
            if low <= tp:
                result = "TP"
                break

    print(f"Entry {direction.upper()} at {price:.2f}, SL {sl:.2f}, TP {tp:.2f} -> {result}")
    timestamp = df.loc[index, "open_time"].isoformat() if "open_time" in df.columns else None
    log_trade(price, direction, sl, tp, result, signal_type, symbol, timestamp)
    return result


def run(signals: List[Dict], df: pd.DataFrame) -> Dict[str, float]:
    """Execute trade simulations using filtered signals."""
    filtered = filter_signals(df, signals)
    tp_count = 0
    sl_count = 0

    for sig in filtered:
        price = float(sig.get("price"))
        direction = str(sig.get("direction"))
        signal_type = str(sig.get("signal_type", ""))
        symbol = str(sig.get("symbol", ""))
        idx = int(sig.get("index", -1))
        result = simulate_trade(df, idx, price, direction, signal_type, symbol)
        if result == "TP":
            tp_count += 1
        else:
            sl_count += 1

    total = tp_count + sl_count
    net_pips = tp_count * TAKE_PROFIT_PIPS - sl_count * STOP_LOSS_PIPS
    return {"tp": tp_count, "sl": sl_count, "total": total, "net_pips": net_pips}


def save_summary(summary: Dict[str, float], path: str) -> None:
    """Save a summary of trading results to a CSV file."""
    total = summary.get("total", 0)
    tp = summary.get("tp", 0)
    sl = summary.get("sl", 0)
    tp_pct = tp / total * 100 if total else 0.0
    sl_pct = sl / total * 100 if total else 0.0
    net_pips = summary.get("net_pips", 0.0)

    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "total": total,
        "tp": tp,
        "sl": sl,
        "tp_pct": f"{tp_pct:.2f}",
        "sl_pct": f"{sl_pct:.2f}",
        "net_pips": f"{net_pips:.2f}",
    }

    file_exists = os.path.isfile(path)
    with open(path, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
