# structure.py
# structure.py

"""Utility functions for detecting BOS and FVG in OHLCV data."""

from typing import Optional, List, Dict
import pandas as pd


def detect_break_of_structure(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    required = {"high", "low"}
    if not required.issubset(df.columns):
        df["bos"] = None
        df["bos_strength"] = 0.0
        return df
    if len(df) < 2:
        df["bos"] = [None] * len(df)
        df["bos_strength"] = [0.0] * len(df)
        return df

    bos: list[Optional[str]] = [None]
    strength: list[float] = [0.0]
    swing_high = float(df.loc[0, "high"])
    swing_low = float(df.loc[0, "low"])

    for i in range(1, len(df)):
        high = float(df.loc[i, "high"])
        low = float(df.loc[i, "low"])
        if high > swing_high:
            bos.append("bullish")
            strength.append(high - swing_high)
            swing_high = high
        elif low < swing_low:
            bos.append("bearish")
            strength.append(swing_low - low)
            swing_low = low
        else:
            bos.append(None)
            strength.append(0.0)

    df["bos"] = bos
    df["bos_strength"] = strength
    return df


def detect_fair_value_gaps(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    required = {"high", "low"}
    if not required.issubset(df.columns):
        df["fvg"] = None
        df["fvg_gap"] = 0.0
        return df
    if len(df) < 3:
        df["fvg"] = [None] * len(df)
        df["fvg_gap"] = [0.0] * len(df)
        return df

    fvg: list[Optional[str]] = [None]
    gap: list[float] = [0.0]

    for i in range(1, len(df) - 1):
        prev_high = float(df.loc[i - 1, "high"])
        prev_low = float(df.loc[i - 1, "low"])
        next_low = float(df.loc[i + 1, "low"])
        next_high = float(df.loc[i + 1, "high"])

        if next_low > prev_high:
            fvg.append("bullish")
            gap.append(next_low - prev_high)
        elif next_high < prev_low:
            fvg.append("bearish")
            gap.append(prev_low - next_high)
        else:
            fvg.append(None)
            gap.append(0.0)

    fvg.append(None)
    gap.append(0.0)

    df["fvg"] = fvg
    df["fvg_gap"] = gap
    return df


def is_strong_candle(row: pd.Series) -> bool:
    body = abs(row["close"] - row["open"])
    range_ = row["high"] - row["low"]
    return range_ > 0 and (body / range_) >= 0.5 and (
        (row["close"] > row["open"]) or (row["close"] < row["open"])
    )


def is_counter_trend(df: pd.DataFrame, idx: int, direction: str) -> bool:
    recent = df[max(0, idx - 3):idx]
    if len(recent) < 3:
        return False
    if direction == "long":
        return all(row["close"] < row["open"] for _, row in recent.iterrows())
    else:
        return all(row["close"] > row["open"] for _, row in recent.iterrows())


def filter_signals(df: pd.DataFrame, signals: List[Dict]) -> List[Dict]:
    filtered = []
    last_entry_idx = -10

    for i in range(len(signals)):
        sig = signals[i]
        if sig["type"] != "BOS" or sig.get("strength", 0.0) < 2.0:
            continue

        direction = sig["direction"]
        for j in range(i + 1, min(i + 4, len(signals))):
            next_sig = signals[j]
            if next_sig["type"] == "FVG" and next_sig["direction"] == direction:
                idx = next_sig["index"]
                if idx >= len(df):
                    continue
                price = df.loc[idx, "close"]
                gap_threshold = 0.005 * price
                if next_sig.get("gap", 0.0) < gap_threshold:
                    continue
                if not is_strong_candle(df.loc[idx]):
                    continue
                if idx - last_entry_idx < 5:
                    continue
                if is_counter_trend(df, idx, direction):
                    continue
                filtered.append({
                    "index": idx,
                    "price": price,
                    "direction": direction,
                    "signal_type": "BOS+FVG"
                })
                last_entry_idx = idx
                break

    return filtered
