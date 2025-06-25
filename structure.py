mport pandas as pd
"""Utility functions for detecting BOS and FVG in OHLCV data."""

from typing import Optional

import pandas as pd


def detect_break_of_structure(df: pd.DataFrame) -> pd.DataFrame:
    """Detect simple Break of Structure (BOS).

    A bullish BOS occurs when price makes a higher high.
    A bearish BOS occurs when price makes a lower low.
    A bullish BOS occurs when price makes a higher high relative to the
    previous swing high. A bearish BOS occurs when price makes a lower low
    relative to the previous swing low.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with at least ``high`` and ``low`` columns.
        DataFrame with ``high`` and ``low`` columns.

    Returns
    -------
    pandas.DataFrame
        The original DataFrame with a new ``bos`` column
        containing ``"bullish"`` or ``"bearish"`` when a BOS is detected.
        Copy of ``df`` with new ``bos`` and ``bos_strength`` columns. ``bos``
        contains ``"bullish"``, ``"bearish"`` or ``None`` for each row. The
        optional ``bos_strength`` metric represents the size of the break.
    The returned frame includes ``bos`` and ``bos_strength`` columns.
    """

    df = df.copy()

    # Validate required columns
    required_cols = {"high", "low"}
    if not required_cols.issubset(df.columns):
        df["bos"] = None
        df["bos_strength"] = 0.0
        return df
    df["bos"] = None
    df["bos_strength"] = 0.0

    if len(df) < 2:
        df["bos"] = [None] * len(df)
        df["bos_strength"] = [0.0] * len(df)
    required = {"high", "low"}
    if not required.issubset(df.columns) or len(df) < 2:
        return df

    bos: list[Optional[str]] = [None]
    swing_high = df['high'].iloc[0]
    swing_low = df['low'].iloc[0]
    strength: list[float] = [0.0]
    swing_high = df["high"].iloc[0]
    swing_low = df["low"].iloc[0]
    swing_high = float(df.loc[0, "high"])
    swing_low = float(df.loc[0, "low"])

    for i in range(1, len(df)):
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        high = df["high"].iloc[i]
        low = df["low"].iloc[i]
        high = float(df.loc[i, "high"])
        low = float(df.loc[i, "low"])

        if high > swing_high:
            bos.append('bullish')
            bos.append("bullish")
            strength.append(high - swing_high)
            df.loc[i, "bos"] = "bullish"
            df.loc[i, "bos_strength"] = high - swing_high
            swing_high = high
        elif low < swing_low:
            bos.append('bearish')
            bos.append("bearish")
            strength.append(swing_low - low)
            df.loc[i, "bos"] = "bearish"
            df.loc[i, "bos_strength"] = swing_low - low
            swing_low = low
        else:
            bos.append(None)
    df['bos'] = bos
            strength.append(0.0)

    df["bos"] = bos
    df["bos_strength"] = strength
    return df


def detect_fair_value_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """Detect 3-candle Fair Value Gaps (FVG).

    A bullish FVG is present when the low of the third candle
    is greater than the high of the first candle.
    A bearish FVG is present when the high of the third candle
    is less than the low of the first candle.
    A bullish FVG is present when the low of the next candle is greater than
    the high of the previous candle. A bearish FVG is present when the high of
    the next candle is less than the low of the previous candle.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with ``high`` and ``low`` columns.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with a new ``fvg`` column indicating
        ``"bullish"`` or ``"bearish"`` FVGs.
        Copy of ``df`` with new ``fvg`` and ``fvg_gap`` columns. ``fvg``
        contains ``"bullish"``, ``"bearish"`` or ``None`` for each row. The
        optional ``fvg_gap`` metric represents the size of the gap.
    A bullish FVG occurs when the low of the next candle is greater than the
    high of the previous candle. A bearish FVG occurs when the high of the next
    candle is less than the low of the previous candle.

    The returned frame includes ``fvg`` and ``fvg_gap`` columns.
    """

    df = df.copy()

    # Validate required columns
    required_cols = {"high", "low"}
    if not required_cols.issubset(df.columns):
        df["fvg"] = None
        df["fvg_gap"] = 0.0
        return df
    df["fvg"] = None
    df["fvg_gap"] = 0.0

    if len(df) < 3:
        df["fvg"] = [None] * len(df)
        df["fvg_gap"] = [0.0] * len(df)
    required = {"high", "low"}
    if not required.issubset(df.columns) or len(df) < 3:
        return df

    fvg: list[Optional[str]] = [None]
    gap: list[float] = [0.0]

    for i in range(1, len(df) - 1):
        prev_high = df['high'].iloc[i - 1]
        next_low = df['low'].iloc[i + 1]
        prev_low = df['low'].iloc[i - 1]
        next_high = df['high'].iloc[i + 1]
        prev_high = df["high"].iloc[i - 1]
        prev_low = df["low"].iloc[i - 1]
        next_low = df["low"].iloc[i + 1]
        next_high = df["high"].iloc[i + 1]
        prev_high = float(df.loc[i - 1, "high"])
        prev_low = float(df.loc[i - 1, "low"])
        next_low = float(df.loc[i + 1, "low"])
        next_high = float(df.loc[i + 1, "high"])

        if next_low > prev_high:
            fvg.append('bullish')
            fvg.append("bullish")
            gap.append(next_low - prev_high)
            df.loc[i, "fvg"] = "bullish"
            df.loc[i, "fvg_gap"] = next_low - prev_high
        elif next_high < prev_low:
            fvg.append('bearish')
            fvg.append("bearish")
            gap.append(prev_low - next_high)
        else:
            fvg.append(None)
            gap.append(0.0)

    fvg.append(None)  # Final row, no 3rd candle
    df['fvg'] = fvg
    # The last row cannot form a 3-candle pattern
    fvg.append(None)
    gap.append(0.0)

    df["fvg"] = fvg
    df["fvg_gap"] = gap
            df.loc[i, "fvg"] = "bearish"
            df.loc[i, "fvg_gap"] = prev_low - next_high

    return df
