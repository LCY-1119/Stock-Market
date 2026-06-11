# -*- coding: utf-8 -*-
"""每日抓取美股数据并写入 data.json,由 GitHub Actions 自动运行。"""

import json
from datetime import datetime, timezone

import yfinance as yf

# 跟踪的标的:代码 -> (显示名, 类型)
TICKERS = {
    "VOO":   ("VOO 标普500 ETF", "holding"),
    "^GSPC": ("标普500指数", "index"),
    "^IXIC": ("纳斯达克综合指数", "index"),
    "^DJI":  ("道琼斯工业指数", "index"),
    "NVDA":  ("英伟达", "watch"),
    "AAPL":  ("苹果", "watch"),
    "TSLA":  ("特斯拉", "watch"),
}

HISTORY_DAYS = "3mo"  # 拉3个月日线,页面画走势图用


def fetch_one(symbol: str, name: str, kind: str):
    t = yf.Ticker(symbol)
    hist = t.history(period=HISTORY_DAYS, interval="1d")
    if hist.empty or len(hist) < 2:
        raise RuntimeError(f"{symbol}: 没有拿到数据")

    closes = hist["Close"].round(2)
    last = float(closes.iloc[-1])
    prev = float(closes.iloc[-2])
    change = last - prev
    change_pct = change / prev * 100

    first = float(closes.iloc[0])
    period_pct = (last - first) / first * 100

    return {
        "symbol": symbol,
        "name": name,
        "kind": kind,
        "price": round(last, 2),
        "change": round(change, 2),
        "change_pct": round(change_pct, 2),
        "period_pct": round(period_pct, 2),
        "dates": [d.strftime("%m-%d") for d in hist.index],
        "closes": [float(c) for c in closes],
    }


def main():
    items = []
    errors = []
    for symbol, (name, kind) in TICKERS.items():
        try:
            items.append(fetch_one(symbol, name, kind))
            print(f"OK  {symbol}")
        except Exception as e:  # 单个失败不影响其他
            errors.append(f"{symbol}: {e}")
            print(f"FAIL {symbol}: {e}")

    if not items:
        raise SystemExit("全部抓取失败,保留旧的 data.json")

    data = {
        "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "items": items,
        "errors": errors,
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"写入 data.json,共 {len(items)} 个标的")


if __name__ == "__main__":
    main()
