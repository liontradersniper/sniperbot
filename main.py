from api import BybitClient
from structure import detect_break_of_structure, detect_fair_value_gaps
from executor import run
from executor import run, save_summary


def get_signals() -> list[dict]:
    """Fetch market data and return BOS/FVG signals."""
    client = BybitClient()
    try:
        df = client.get_ohlcv("BTCUSDT")
    except Exception as exc:
        print(f"Error fetching data: {exc}")
        return []

    if df is None or df.empty:
        print("No data retrieved")
        return []

    try:
        df = detect_break_of_structure(df)
        df = detect_fair_value_gaps(df)
    except Exception as exc:
        print(f"Error processing data: {exc}")
        return []

    signals = []
    for _, row in df.iterrows():
        if row.get("bos"):
            signals.append(
                {
                    "price": float(row["close"]),
                    "direction": "long" if row["bos"] == "bullish" else "short",
                    "signal_type": "BOS",
                    "symbol": "BTCUSDT",
                }
            )
        if row.get("fvg"):
            signals.append(
                {
                    "price": float(row["close"]),
                    "direction": "long" if row["fvg"] == "bullish" else "short",
                    "signal_type": "FVG",
                    "symbol": "BTCUSDT",
                }
            )
    return signals


if __name__ == "__main__":
    print("Starting trading simulation on BTCUSDT (5m)")
    signals = get_signals()
    run(signals)
    summary = run(signals)

    total = summary.get("total", 0)
    if total:
        tp = summary.get("tp", 0)
        sl = summary.get("sl", 0)
        tp_pct = tp / total * 100
        sl_pct = sl / total * 100
        net_pips = summary.get("net_pips", 0)

        print("\nSimulation Summary:")
        print(f"Total trades: {total}")
        print(f"Take Profit: {tp} ({tp_pct:.2f}%)")
        print(f"Stop Loss: {sl} ({sl_pct:.2f}%)")
        print(f"Net result: {net_pips:.2f} pips")
    else:
        print("No trades executed.")

    save_summary(summary, "summary.csv")
