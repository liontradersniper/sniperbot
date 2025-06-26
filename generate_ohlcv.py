# generate_ohlcv.py
"""Generate a synthetic OHLCV dataset for Sniperbot backtesting."""

from __future__ import annotations

import os
import random
from datetime import datetime, timedelta
from typing import List

import pandas as pd


def generate_ohlcv(
    start_price: float = 10000.0,
    candles: int = 1000,
    interval: timedelta = timedelta(minutes=5),
) -> pd.DataFrame:
    """Return a DataFrame containing synthetic OHLCV data."""

    start_time = datetime.utcnow() - candles * interval

    times: List[str] = []
    opens: List[float] = []
    highs: List[float] = []
    lows: List[float] = []
    closes: List[float] = []
    volumes: List[float] = []

    close_price = start_price

    for i in range(candles):
        open_time = start_time + i * interval
        open_price = close_price
        close_price = open_price + random.gauss(0, 20)
        high = max(open_price, close_price) + abs(random.gauss(0, 10))
        low = min(open_price, close_price) - abs(random.gauss(0, 10))
        volume = random.uniform(1, 10)

        times.append(open_time.isoformat())
        opens.append(open_price)
        highs.append(high)
        lows.append(low)
        closes.append(close_price)
        volumes.append(volume)

    df = pd.DataFrame(
        {
            "open_time": times,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
        }
    )
    return df


if __name__ == "__main__":
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    df = generate_ohlcv()
    output_path = os.path.join(output_dir, "ohlcv.csv")
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} candles to {output_path}")
