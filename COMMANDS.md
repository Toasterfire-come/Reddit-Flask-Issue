# Command Reference Guide

## Two Main Commands

### Command 1: Retrieve Stock Data (300+ NYSE & NASDAQ)

```bash
python3 market_manager.py
```

**What it does:**
- Fetches market data for 300+ stocks from NYSE and NASDAQ
- Saves to `json/stock_data_export.json`
- Includes proxy support (configurable)
- Automatic retry logic for failed requests

**Stock Coverage:**
- **NASDAQ (150+ stocks)**: Tech, Software, Semiconductors, Biotech, E-commerce
- **NYSE (150+ stocks)**: Financial Services, Healthcare, Consumer Goods, Energy, Industrials, Utilities, REITs

---

### Command 2: Deploy to SFTP

```bash
./deploy.sh
```

**What it does:**
- Pulls latest code from GitHub repository
- Installs Python dependencies
- Uploads all files to SFTP server

**Pre-configured with:**
- Host: `access-5018544625.webspace-host.com`
- User: `a1531117`
- Password: `C2rt3rK#2010`
- Port: `22` (SFTP + SSH)

---

## Complete Workflow

### Step 1: Retrieve Market Data

```bash
python3 market_manager.py
```

Output:
```
======================================================================
  Market Manager - NYSE & NASDAQ Data Retrieval
======================================================================

Initializing market data retrieval...
Total tickers: 300

Fetching market data for all tickers...
Starting data retrieval for 300 tickers...
[1/300] Fetching AAPL... ✓
[2/300] Fetching MSFT... ✓
[3/300] Fetching GOOGL... ✓
...

Completed: 300/300 tickers retrieved successfully

Saving data to json/stock_data_export.json...
Data saved to json/stock_data_export.json

======================================================================
✓ Market Manager Complete!
  Retrieved: 300 tickers
  Output: json/stock_data_export.json
======================================================================
```

### Step 2: Deploy to SFTP

```bash
./deploy.sh
```

Output:
```
================================================================================
  SFTP Deployment
================================================================================

Deploying to SFTP
================================================================================
Repository: https://github.com/Toasterfire-come/Reddit-Flask-Issue.git
Branch: main
SFTP Host: access-5018544625.webspace-host.com
SFTP User: a1531117
Remote Path: /

[INFO] Working directory: /tmp/sftp_deploy_xyz123
[INFO] Cloning repository: https://github.com/Toasterfire-come/Reddit-Flask-Issue.git
✓ Git clone successful
...
✓ DEPLOYMENT SUCCESSFUL!

================================================================================
  SFTP Deployment Complete!
================================================================================
✓ Project deployed to SFTP server
  Host: access-5018544625.webspace-host.com
  Path: /
```

---

## Stock Ticker Coverage

### NASDAQ (150+ stocks)

**Technology Giants:**
- AAPL, MSFT, GOOGL, GOOG, AMZN, META, NVDA, TSLA, AVGO, ADBE, NFLX, CSCO, INTC, AMD, QCOM, TXN, AMAT, MU, ADI, LRCX

**Software & Cloud:**
- CRM, ORCL, ADSK, INTU, ANSS, CTSH, EA, TTWO, NOW, WDAY, SNOW, PLTR, DOCU, ZM, OKTA, VEEV

**Semiconductors:**
- TSM, ASML, NXPI, MRVL, ON, MPWR, SWKS, QRVO

**Biotech & Healthcare:**
- AMGN, GILD, VRTX, REGN, BIIB, ILMN, MRNA, BNTX, ALNY, SGEN

**E-commerce & Consumer:**
- EBAY, BKNG, ETSY, MELI, SE, ABNB, DASH

### NYSE (150+ stocks)

**Financial Services:**
- JPM, BAC, WFC, C, GS, MS, BLK, SCHW, USB, PNC, TFC, COF, AXP, BK, STT

**Payment Networks:**
- V, MA, PYPL, SQ, FIS, FISV, FLT, GPN

**Insurance:**
- BRK.B, PGR, CB, TRV, ALL, AIG, MET, PRU, AFL

**Healthcare & Pharma:**
- JNJ, UNH, PFE, ABBV, TMO, MRK, ABT, DHR, BMY, LLY, CVS, CI, HUM

**Consumer Goods & Retail:**
- WMT, HD, PG, KO, PEP, COST, NKE, MCD, SBUX, TGT, LOW, TJX, DG

**Energy:**
- XOM, CVX, COP, SLB, EOG, MPC, PSX, VLO, OXY, HAL

**Industrials:**
- BA, CAT, GE, MMM, HON, UPS, RTX, LMT, DE, EMR

**Materials:**
- LIN, APD, ECL, SHW, DD, NEM, FCX, NUE

**Real Estate (REITs):**
- AMT, PLD, CCI, EQIX, PSA, DLR, SPG, O, WELL, AVB

**Utilities:**
- NEE, DUK, SO, D, AEP, EXC, SRE, PEG

---

## Advanced Usage

### Deploy Different Branch

```bash
./deploy.sh --branch dev
```

### Deploy to Different Path

```bash
./deploy.sh --remote-path /public_html
```

### Use Different Repository

```bash
./deploy.sh --repo https://github.com/yourusername/another-repo.git
```

---

## Automation with Cron

### Daily Market Data Updates

```bash
# Run Monday-Friday at 6 PM (after market close)
0 18 * * 1-5 cd /path/to/Reddit-Flask-Issue && python3 market_manager.py >> /var/log/market_data.log 2>&1
```

### Daily Deployment

```bash
# Deploy at 6:30 PM after data retrieval
30 18 * * 1-5 cd /path/to/Reddit-Flask-Issue && ./deploy.sh >> /var/log/sftp_deploy.log 2>&1
```

Edit crontab:
```bash
crontab -e
```

---

## Files Created

### After market_manager.py

```
json/
├── stock_data_export.json          # Latest market data (300+ stocks)
└── backups/
    └── stock_data_YYYYMMDD_HHMMSS.json  # Timestamped backups
```

### After deploy.sh

All project files uploaded to SFTP server root directory:
- App.py
- market_manager.py
- market_data_retrieval.py
- Templates/
- json/
- requirements.txt

---

## Troubleshooting

### Market Manager Issues

Check files exist:
```bash
ls -la market_manager.py market_data_retrieval.py
```

Test retrieval:
```bash
python3 market_manager.py
```

Check output:
```bash
cat json/stock_data_export.json | python3 -m json.tool | head -50
```

### SFTP Deployment Issues

Test SFTP connection:
```bash
sftp -P 22 a1531117@access-5018544625.webspace-host.com
# Password: C2rt3rK#2010
```

Check Python:
```bash
python3 --version
pip3 list | grep -E "paramiko|yfinance|pandas"
```

---

## Quick Reference Table

| Task | Command |
|------|---------|
| **Retrieve 300+ NYSE/NASDAQ stocks** | `python3 market_manager.py` |
| **Deploy to SFTP** | `./deploy.sh` |
| Deploy different branch | `./deploy.sh --branch branch-name` |
| Run Flask app locally | `python3 App.py` |
| Check data file | `ls -lh json/stock_data_export.json` |

---

## Summary

```bash
# 1. Retrieve market data for 300+ stocks
python3 market_manager.py

# 2. Deploy to SFTP
./deploy.sh
```

Done! Your Flask app with fresh market data is deployed to your webspace.
