import random
from typing import List, Dict
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


def run(signals: List[Dict]) -> None:
    """Execute trade simulations for a list of signals."""
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
        simulate_trade(price, direction, signal_type, symbol)
        result = simulate_trade(price, direction, signal_type, symbol)
        if result == "TP":
            tp_count += 1
        else:
            sl_count += 1

    total = tp_count + sl_count
    net_pips = tp_count * TAKE_PROFIT_PIPS - sl_count * STOP_LOSS_PIPS
    return {"tp": tp_count, "sl": sl_count, "total": total, "net_pips": net_pips}
