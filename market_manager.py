#!/usr/bin/env python3
"""
Market Manager - Standalone Script
Retrieves market data for 300+ NYSE and NASDAQ stocks
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from market_data_retrieval import MarketDataRetrieval

def main():
    """Run the market data retrieval script"""
    print("=" * 70)
    print("  Market Manager - NYSE & NASDAQ Data Retrieval")
    print("=" * 70)
    print()

    # Configure proxies if needed (optional)
    proxies = [
        # Add your proxy list here if needed
        # "http://proxy1.example.com:8080",
        # "http://proxy2.example.com:8080",
    ]

    # Initialize retrieval system
    print("Initializing market data retrieval...")
    retrieval = MarketDataRetrieval(proxy_list=proxies if proxies else None)

    print(f"Total tickers: {len(retrieval.tickers)}")
    print()

    # Fetch data
    print("Fetching market data for all tickers...")
    data = retrieval.fetch_all_tickers(delay=0.5, max_retries=3)

    if not data:
        print("\n✗ Failed to retrieve market data")
        sys.exit(1)

    # Save to JSON
    print("\nSaving data to json/stock_data_export.json...")
    retrieval.save_to_json(data)

    print("\n" + "=" * 70)
    print("✓ Market Manager Complete!")
    print(f"  Retrieved: {len(data)} tickers")
    print(f"  Output: json/stock_data_export.json")
    print("=" * 70)

    sys.exit(0)


if __name__ == "__main__":
    main()
