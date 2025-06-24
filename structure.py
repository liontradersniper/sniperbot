import pandas as pd
from typing import Optional


def detect_break_of_structure(df: pd.DataFrame) -> pd.DataFrame:
    """Detect simple Break of Structure (BOS).

    A bullish BOS occurs when price makes a higher high.
    A bearish BOS occurs when price makes a lower low.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with at least ``high`` and ``low`` columns.

    Returns
    -------
    pandas.DataFrame
        The original DataFrame with a new ``bos`` column
        containing ``"bullish"`` or ``"bearish"`` when a BOS is detected.
    """
    df = df.copy()
    bos: list[Optional[str]] = [None]
    swing_high = df['high'].iloc[0]
    swing_low = df['low'].iloc[0]
    strength: list[float] = [0.0]
    swing_high = df["high"].iloc[0]
    swing_low = df["low"].iloc[0]

    for i in range(1, len(df)):
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        if high > swing_high:
            bos.append('bullish')
            bos.append("bullish")
            strength.append(high - swing_high)
            swing_high = high
        elif low < swing_low:
            bos.append('bearish')
            bos.append("bearish")
            strength.append(swing_low - low)
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

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with ``high`` and ``low`` columns.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with a new ``fvg`` column indicating
        ``"bullish"`` or ``"bearish"`` FVGs.
    """
    df = df.copy()
    fvg: list[Optional[str]] = [None]
    gap: list[float] = [0.0]

    for i in range(1, len(df) - 1):
        prev_high = df['high'].iloc[i - 1]
        next_low = df['low'].iloc[i + 1]
        prev_low = df['low'].iloc[i - 1]
        next_high = df['high'].iloc[i + 1]

        if next_low > prev_high:
            fvg.append('bullish')
            fvg.append("bullish")
            gap.append(next_low - prev_high)
        elif next_high < prev_low:
            fvg.append('bearish')
            fvg.append("bearish")
            gap.append(prev_low - next_high)
        else:
            fvg.append(None)
            gap.append(0.0)

    fvg.append(None)  # Final row, no 3rd candle
    df['fvg'] = fvg
    gap.append(0.0)
    df["fvg"] = fvg
    df["fvg_gap"] = gap
    return df
