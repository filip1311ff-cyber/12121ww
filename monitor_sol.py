"""Simple script to monitor the SOL (Solana) price.

The script fetches the current price from the CoinGecko API and prints it
periodically.  It keeps the implementation intentionally lightweight, relying
only on the standard library in addition to ``requests`` for HTTP calls.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict

import requests

API_URL = "https://api.coingecko.com/api/v3/simple/price"
COIN_ID = "solana"
CURRENCY = "usd"


def fetch_sol_price() -> float:
    """Fetch the latest SOL price in USD from CoinGecko."""
    response = requests.get(
        API_URL,
        params={"ids": COIN_ID, "vs_currencies": CURRENCY},
        timeout=10,
    )
    response.raise_for_status()
    data: Dict[str, Dict[str, Any]] = response.json()
    try:
        return float(data[COIN_ID][CURRENCY])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("Unexpected response structure from CoinGecko") from exc


def log_price(price: float) -> None:
    """Print the price with an ISO 8601 timestamp."""
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] SOL price: ${price:,.2f}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor SOL price in USD")
    parser.add_argument(
        "--interval",
        type=float,
        default=60.0,
        help="Polling interval in seconds (default: 60)",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=0,
        help="Number of iterations to run (0 means run until interrupted)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    interval = max(args.interval, 1.0)
    iterations = args.iterations

    remaining = iterations if iterations > 0 else None

    try:
        while remaining is None or remaining > 0:
            price = fetch_sol_price()
            log_price(price)

            if remaining is not None:
                remaining -= 1
                if remaining == 0:
                    break

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except requests.RequestException as exc:
        print(f"Failed to fetch SOL price: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
