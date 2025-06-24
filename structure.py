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

    for i in range(1, len(df)):
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        if high > swing_high:
            bos.append('bullish')
            swing_high = high
        elif low < swing_low:
            bos.append('bearish')
            swing_low = low
        else:
            bos.append(None)
    df['bos'] = bos
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

    for i in range(1, len(df) - 1):
        prev_high = df['high'].iloc[i - 1]
        next_low = df['low'].iloc[i + 1]
        prev_low = df['low'].iloc[i - 1]
        next_high = df['high'].iloc[i + 1]

        if next_low > prev_high:
            fvg.append('bullish')
        elif next_high < prev_low:
            fvg.append('bearish')
        else:
            fvg.append(None)

    fvg.append(None)  # Final row, no 3rd candle
    df['fvg'] = fvg
    return df
