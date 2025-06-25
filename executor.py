"""Utilities for simulating trade execution in Sniperbot."""

import csv
import os
import random
from datetime import datetime
from typing import Dict, List
import os
import csv
import pandas as pd

from logger import log_trade

STOP_LOSS_PIPS = 10
TAKE_PROFIT_PIPS = 20


def simulate_trade(price: float, direction: str, signal_type: str = "", symbol: str = "") -> str:
    """Simulate a trade and log the result.
def simulate_trade(
    df: pd.DataFrame,
    index: int,
    price: float,
    direction: str,
    signal_type: str = "",
    symbol: str = "",
    lookahead: int = 3,
) -> str:
    """Simulate a trade based on subsequent candle data and log the result.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing OHLCV data.
    index : int
        Row index where the trade is opened.
    price : float
        Entry price of the trade.
    direction : str
        "long" or "short".
    signal_type : str, optional
        The type of trading signal.
    symbol : str, optional
        The traded symbol.

    Returns
    -------
    str
        Either "TP" if take profit was hit first or "SL" otherwise.
        Either ``"TP"`` if take profit was hit first or ``"SL"`` otherwise.
    """
    """Simulate a trade based on subsequent candle data and log the result."""

    direction = direction.lower()
    if direction not in {"long", "short"}:
        raise ValueError("direction must be 'long' or 'short'")

    if direction == "long":
        sl = price - STOP_LOSS_PIPS
        tp = price + TAKE_PROFIT_PIPS
    else:
        sl = price + STOP_LOSS_PIPS
        tp = price - TAKE_PROFIT_PIPS

    result = random.choice(["TP", "SL"])
    print(f"Entry {direction.upper()} at {price:.2f}, SL {sl:.2f}, TP {tp:.2f} -> {result}")
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
    print(
        f"Entry {direction.upper()} at {price:.2f}, SL {sl:.2f}, TP {tp:.2f} -> {result}"

    timestamp = (
        df.loc[index, "open_time"].isoformat() if "open_time" in df.columns else None
    )
    log_trade(price, direction, sl, tp, result, signal_type, symbol)
    print(f"Entry {direction.upper()} at {price:.2f}, SL {sl:.2f}, TP {tp:.2f} -> {result}")
    log_trade(price, direction, sl, tp, result, signal_type, symbol, timestamp)
    return result
def run(signals: List[Dict]) -> Dict[str, float]:
def run(signals: List[Dict], df: pd.DataFrame) -> Dict[str, float]:
    """Execute trade simulations and return summary statistics.

    Parameters
    ----------
    signals : list[dict]
        Trading signals produced by the strategy.
    df : pandas.DataFrame
        OHLCV data corresponding to the signals.

    Returns
    -------
    dict
        Summary statistics with keys ``tp``, ``sl``, ``total``, and ``net_pips``.
    """
def run(signals: List[Dict], df: pd.DataFrame) -> Dict[str, float]:
    """Execute trade simulations and return summary statistics."""

    tp_count = 0
    sl_count = 0

    for sig in signals:
        price = float(sig.get("price"))
        direction = str(sig.get("direction"))
        signal_type = str(sig.get("signal_type", ""))
        symbol = str(sig.get("symbol", ""))
        result = simulate_trade(price, direction, signal_type, symbol)
        idx = int(sig.get("index", -1))
        result = simulate_trade(df, idx, price, direction, signal_type, symbol)
        if result == "TP":
            tp_count += 1
        else:
            sl_count += 1

    total = tp_count + sl_count
    net_pips = tp_count * TAKE_PROFIT_PIPS - sl_count * STOP_LOSS_PIPS
    return {"tp": tp_count, "sl": sl_count, "total": total, "net_pips": net_pips}


def save_summary(summary: Dict[str, int], path: str) -> None:
    """Save a summary of trading results to a CSV file.

    Parameters
    ----------
    summary : dict
        Output dictionary from :func:`run`.
    path : str
        CSV file path to append the summary.
    """
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
