"""Utility functions for detecting BOS and FVG in OHLCV data."""

from typing import Optional

import pandas as pd


def detect_break_of_structure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect simple Break of Structure (BOS).

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with ``high`` and ``low`` columns.

    Returns
    -------
    pandas.DataFrame
        Copy of ``df`` with new ``bos`` and ``bos_strength`` columns. ``bos``
        contains ``"bullish"``, ``"bearish"`` or ``None`` for each row. The
        ``bos_strength`` column represents the size of the break.
    """
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
    """
    Detect 3-candle Fair Value Gaps (FVG).

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with ``high`` and ``low`` columns.

    Returns
    -------
    pandas.DataFrame
        Copy of ``df`` with new ``fvg`` and ``fvg_gap`` columns. ``fvg`` contains
        ``"bullish"``, ``"bearish"`` or ``None`` for each row. ``fvg_gap``
        represents the size of the gap when present.
    """
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

    # Append placeholder for final row which cannot form a pattern
    fvg.append(None)
    gap.append(0.0)

    df["fvg"] = fvg
    df["fvg_gap"] = gap
    return df
