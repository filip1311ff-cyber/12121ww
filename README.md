# SOL Price Monitor

This repository contains a lightweight Python script for monitoring the Solana
(SOL) price in USD using the public CoinGecko API.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the monitor (adjust the polling interval or iteration count if desired):
   ```bash
   python monitor_sol.py --interval 30 --iterations 10
   ```

   Omitting `--iterations` (or leaving it as `0`) keeps the script running until
   you stop it manually.

The script prints the current SOL price together with an ISO 8601 timestamp for
each poll.
