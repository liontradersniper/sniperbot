from api import BybitClient
from structure import detect_break_of_structure, detect_fair_value_gaps
from executor import run

import os


def get_signals() -> list[dict]:
    """Process market data and return a list of signals for execution.

    Returns
    -------
    list of dict
        Each dict represents a signal with price, direction, signal_type, and symbol.
    """
    client = BybitClient()
    df = client.get_ohlcv("BTCUSDT")

    df = detect_break_of_structure(df)
    df = detect_fair_value_gaps(df)

    signals = []
    for _, row in df.iterrows():
        if row.get("bos"):
            signals.append({
                "price": float(row["close"]),
                "direction": "long" if row["bos"] == "bullish" else "short",
                "signal_type": "BOS",
                "symbol": "BTCUSDT"
            })
        if row.get("fvg"):
            signals.append({
                "price": float(row["close"]),
                "direction": "long" if row["fvg"] == "bullish" else "short",
                "signal_type": "FVG",
                "symbol": "BTCUSDT"
            })

    return signals


if __name__ == "__main__":
    print("Running ZoharBot ICT simulation on BTCUSDT - 5m timeframe")
    signals = get_signals()
    run(signals)
