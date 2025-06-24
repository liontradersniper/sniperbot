"""Utilities for simulating trade execution in Sniperbot."""

import csv
import os
import random
from typing import Dict, List

from logger import log_trade

STOP_LOSS_PIPS = 10
TAKE_PROFIT_PIPS = 20


def simulate_trade(price: float, direction: str, signal_type: str = "", symbol: str = "") -> str:
    """Simulate a trade and log the result.

    Parameters
    ----------
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
    """
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
    log_trade(price, direction, sl, tp, result, signal_type, symbol)
    return result
def run(signals: List[Dict]) -> Dict[str, float]:
    """Execute trade simulations and return summary statistics.

    Parameters
    ----------
    signals : list[dict]
        Trading signals produced by the strategy.

    Returns
    -------
    dict
        Summary statistics with keys ``tp``, ``sl``, ``total``, and ``net_pips``.
    """

    tp_count = 0
    sl_count = 0

    for sig in signals:
        price = float(sig.get("price"))
        direction = str(sig.get("direction"))
        signal_type = str(sig.get("signal_type", ""))
        symbol = str(sig.get("symbol", ""))
        result = simulate_trade(price, direction, signal_type, symbol)
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

    total = summary.get("total", 0)
    tp = summary.get("tp", 0)
    sl = summary.get("sl", 0)
    tp_pct = tp / total * 100 if total else 0.0
    sl_pct = sl / total * 100 if total else 0.0
    net_pips = summary.get("net_pips", 0)

    file_exists = os.path.isfile(path)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["total", "tp", "sl", "tp_pct", "sl_pct", "net_pips"]
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "total": total,
                "tp": tp,
                "sl": sl,
                "tp_pct": f"{tp_pct:.2f}",
                "sl_pct": f"{sl_pct:.2f}",
                "net_pips": f"{net_pips:.2f}",
            }
        )
