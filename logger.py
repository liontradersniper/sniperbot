# logger.py
import csv
import os
from datetime import datetime
from typing import Optional


LOG_FILE = "trade_log.csv"


def log_trade(
    price: float,
    direction: str,
    sl: float,
    tp: float,
    result: str,
    signal_type: str,
    symbol: str,
    timestamp: Optional[str] = None
) -> None:
    """Log a simulated trade to a CSV file.

    Parameters
    ----------
    price : float
        Entry price.
    direction : str
        'long' or 'short'.
    sl : float
        Stop Loss price.
    tp : float
        Take Profit price.
    result : str
        Trade result: 'TP' or 'SL'.
    signal_type : str
        Type of signal used: 'BOS', 'FVG', etc.
    symbol : str
        Symbol traded, e.g. BTCUSDT.
    timestamp : str, optional
        ISO timestamp. If None, current time is used.
    """
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()

    row = {
        "timestamp": timestamp,
        "symbol": symbol,
        "direction": direction,
        "price": price,
        "stop_loss": sl,
        "take_profit": tp,
        "result": result,
        "signal_type": signal_type,
    }

    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
