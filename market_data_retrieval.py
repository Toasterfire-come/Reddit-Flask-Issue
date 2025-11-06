"""
Market Data Retrieval Script with Proxy Support
Fetches stock market data for 300+ NYSE and NASDAQ tickers using rotating proxies
"""

import yfinance as yf
import pandas as pd
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class MarketDataRetrieval:
    """Handles market data retrieval with proxy rotation and error handling"""

    def __init__(self, proxy_list: Optional[List[str]] = None):
        """
        Initialize the market data retrieval system

        Args:
            proxy_list: List of proxy URLs in format 'http://ip:port'
        """
        self.proxy_list = proxy_list or []
        self.current_proxy_index = 0
        self.session = self._create_session()

        # Comprehensive NYSE and NASDAQ ticker list (300+ stocks)
        self.tickers = [
            # === NASDAQ - Technology Giants ===
            "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA", "AVGO", "ADBE",
            "NFLX", "CSCO", "INTC", "AMD", "QCOM", "TXN", "AMAT", "MU", "ADI", "LRCX",
            "KLAC", "SNPS", "CDNS", "MCHP", "FTNT", "PANW", "CRWD", "ZS", "NET", "DDOG",
            "TEAM", "NOW", "WDAY", "SNOW", "PLTR", "U", "DKNG", "RBLX", "ABNB", "DASH",

            # === NASDAQ - Software & Cloud ===
            "CRM", "ORCL", "ADSK", "INTU", "ANSS", "CTSH", "EA", "TTWO", "ATVI", "DOCU",
            "ZM", "OKTA", "CRWD", "DBX", "BOX", "VEEV", "RNG", "SMAR", "PCTY", "ZUO",

            # === NASDAQ - Semiconductors ===
            "TSM", "ASML", "NXPI", "MRVL", "ON", "MPWR", "SWKS", "QRVO", "WOLF", "SITM",

            # === NASDAQ - Biotech & Healthcare ===
            "AMGN", "GILD", "VRTX", "REGN", "BIIB", "ILMN", "MRNA", "BNTX", "ALNY", "SGEN",
            "INCY", "NBIX", "EXEL", "BMRN", "SRPT", "IONS", "JAZZ", "UTHR", "RARE", "FOLD",

            # === NASDAQ - E-commerce & Consumer ===
            "EBAY", "BKNG", "TRIP", "GRUB", "CHGG", "CVNA", "W", "ETSY", "MELI", "SE",

            # === NASDAQ - Communications ===
            "CMCSA", "CHTR", "DISH", "SIRI", "LBRDA", "LBRDK", "FYBR", "CABO", "LUMN", "T",

            # === NYSE - Financial Services ===
            "JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "SCHW", "USB", "PNC",
            "TFC", "COF", "AXP", "BK", "STT", "NTRS", "CFG", "KEY", "FITB", "RF",
            "HBAN", "CMA", "ZION", "EWBC", "SBNY", "MTB", "FHN", "WAL", "ONB", "CBSH",

            # === NYSE - Payment Networks ===
            "V", "MA", "PYPL", "SQ", "FIS", "FISV", "FLT", "GPN", "JKHY", "ADS",

            # === NYSE - Insurance ===
            "BRK.B", "PGR", "CB", "TRV", "ALL", "AIG", "MET", "PRU", "AFL", "AMP",
            "HIG", "PFG", "LNC", "GL", "AIZ", "WRB", "RGA", "TMK", "AFG", "Y",

            # === NYSE - Healthcare & Pharma ===
            "JNJ", "UNH", "PFE", "ABBV", "TMO", "MRK", "ABT", "DHR", "BMY", "LLY",
            "CVS", "CI", "HUM", "ANTM", "CNC", "MOH", "ELV", "HCA", "UHS", "THC",
            "CYH", "LPNT", "MD", "CHE", "RDNT", "USPH", "ENSG", "DVA", "AMN", "AHS",

            # === NYSE - Consumer Goods & Retail ===
            "WMT", "HD", "PG", "KO", "PEP", "COST", "NKE", "MCD", "SBUX", "TGT",
            "LOW", "TJX", "DG", "DLTR", "BBY", "GPS", "M", "KSS", "JWN", "ROST",
            "AZO", "ORLY", "AAP", "GPC", "DKS", "FL", "FIVE", "OLLI", "BURL", "BJ",

            # === NYSE - Food & Beverage ===
            "PM", "MO", "STZ", "TAP", "BF.B", "SAM", "MNST", "KDP", "CELH", "FIZZ",
            "CLX", "CHD", "SPB", "EL", "CL", "KMB", "SJM", "CAG", "GIS", "K",

            # === NYSE - Energy ===
            "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "HAL",
            "BKR", "PXD", "DVN", "FANG", "HES", "MRO", "APA", "OVV", "CTRA", "NOG",
            "XEC", "SM", "MGY", "PR", "RRC", "MTDR", "AR", "CHRD", "VTLE", "CLR",

            # === NYSE - Industrials ===
            "BA", "CAT", "GE", "MMM", "HON", "UPS", "RTX", "LMT", "DE", "EMR",
            "ETN", "ITW", "PH", "CMI", "EMR", "ROK", "AME", "DOV", "XYL", "IEX",
            "FLS", "VLTO", "IR", "FAST", "J", "SNA", "GGG", "PCAR", "NSC", "UNP",

            # === NYSE - Materials ===
            "LIN", "APD", "ECL", "SHW", "DD", "NEM", "FCX", "NUE", "VMC", "MLM",
            "PKG", "IP", "WRK", "SLVM", "SEE", "AVY", "BALL", "CCK", "OLN", "EMN",

            # === NYSE - Real Estate (REITs) ===
            "AMT", "PLD", "CCI", "EQIX", "PSA", "DLR", "SPG", "O", "WELL", "AVB",
            "EQR", "VTR", "ARE", "MAA", "ESS", "UDR", "CPT", "ELS", "SUI", "STAG",

            # === NYSE - Utilities ===
            "NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "PEG", "XEL", "ED",
            "WEC", "ES", "DTE", "EIX", "PPL", "FE", "AEE", "CMS", "CNP", "NI",

            # === NYSE - Telecommunications ===
            "VZ", "TMUS", "T", "VOD", "BCE", "TEF", "TU", "AMX", "VIV", "ORAN"
        ]

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _get_next_proxy(self) -> Optional[Dict[str, str]]:
        """Get the next proxy from the rotation"""
        if not self.proxy_list:
            return None

        proxy_url = self.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)

        return {
            'http': proxy_url,
            'https': proxy_url
        }

    def fetch_ticker_data(self, ticker: str, use_proxy: bool = True) -> Optional[Dict]:
        """
        Fetch data for a single ticker

        Args:
            ticker: Stock ticker symbol
            use_proxy: Whether to use proxy rotation

        Returns:
            Dictionary with stock data or None if failed
        """
        try:
            # Configure proxy if available and requested
            proxy = self._get_next_proxy() if use_proxy and self.proxy_list else None

            # Fetch ticker data
            stock = yf.Ticker(ticker, session=self.session)
            info = stock.info
            hist = stock.history(period="3mo")

            # Calculate metrics
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            previous_close = info.get('previousClose', 0)
            price_change = current_price - previous_close if previous_close else 0
            price_change_pct = (price_change / previous_close * 100) if previous_close else 0

            # Market cap change (3 months)
            market_cap = info.get('marketCap', 0)
            market_cap_3mo_change = 0
            if len(hist) > 0:
                price_3mo_ago = hist.iloc[0]['Close'] if not hist.empty else current_price
                market_cap_3mo_change = ((current_price - price_3mo_ago) / price_3mo_ago * 100) if price_3mo_ago else 0

            # Build data dictionary
            data = {
                "Ticker": ticker,
                "Company Name": info.get('longName', ticker),
                "Current Price": round(current_price, 2),
                "Previous Close": round(previous_close, 2),
                "Price Change": round(price_change, 2),
                "Price Change (%)": round(price_change_pct, 2),
                "Volume": info.get('volume', 0),
                "Average Volume": info.get('averageVolume', 0),
                "Market Cap": market_cap,
                "Market Cap Change (3 Mon)": round(market_cap_3mo_change, 2),
                "PE Ratio": round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 0,
                "EPS": round(info.get('trailingEps', 0), 2) if info.get('trailingEps') else 0,
                "52 Week High": round(info.get('fiftyTwoWeekHigh', 0), 2),
                "52 Week Low": round(info.get('fiftyTwoWeekLow', 0), 2),
                "Dividend Yield": round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0,
                "Sector": info.get('sector', 'N/A'),
                "Industry": info.get('industry', 'N/A'),
                "Shares Available": info.get('sharesOutstanding', 0),
                "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            return data

        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            return None

    def fetch_all_tickers(self, delay: float = 0.5, max_retries: int = 3) -> List[Dict]:
        """
        Fetch data for all tickers with rate limiting and retries

        Args:
            delay: Delay between requests in seconds
            max_retries: Maximum number of retries per ticker

        Returns:
            List of stock data dictionaries
        """
        all_data = []
        total_tickers = len(self.tickers)

        print(f"Starting data retrieval for {total_tickers} tickers...")
        print(f"Using {len(self.proxy_list)} proxies" if self.proxy_list else "No proxies configured")

        for idx, ticker in enumerate(self.tickers, 1):
            print(f"[{idx}/{total_tickers}] Fetching {ticker}...", end=" ")

            data = None
            for attempt in range(max_retries):
                data = self.fetch_ticker_data(ticker, use_proxy=bool(self.proxy_list))

                if data:
                    print("✓")
                    all_data.append(data)
                    break
                else:
                    if attempt < max_retries - 1:
                        print(f"✗ (retry {attempt + 1}/{max_retries})", end=" ")
                        time.sleep(delay * 2)  # Longer delay on retry
                    else:
                        print("✗ (failed)")

            # Rate limiting
            if idx < total_tickers:
                time.sleep(delay + random.uniform(0, 0.3))  # Add jitter

        print(f"\nCompleted: {len(all_data)}/{total_tickers} tickers retrieved successfully")
        return all_data

    def save_to_json(self, data: List[Dict], output_path: str = "json/stock_data_export.json"):
        """
        Save data to JSON file

        Args:
            data: List of stock data dictionaries
            output_path: Path to output JSON file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Data saved to {output_path}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")

    def add_tickers(self, new_tickers: List[str]):
        """Add additional tickers to the retrieval list"""
        self.tickers.extend([t.upper() for t in new_tickers if t.upper() not in self.tickers])
        print(f"Updated ticker list: {len(self.tickers)} total tickers")


if __name__ == "__main__":
    # Example usage
    # Configure proxies (optional)
    proxies = [
        # Add your proxy list here
        # "http://proxy1.example.com:8080",
        # "http://proxy2.example.com:8080",
    ]

    # Initialize retrieval system
    retrieval = MarketDataRetrieval(proxy_list=proxies if proxies else None)

    # Fetch data
    data = retrieval.fetch_all_tickers(delay=0.5, max_retries=3)

    # Save to JSON
    retrieval.save_to_json(data)

    print("\n✓ Market data retrieval complete!")
