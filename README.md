# Stock Market Data Filter & Retrieval System

Flask-based stock market data filtering application with automated retrieval of 300+ NYSE and NASDAQ stocks and SFTP deployment.

## Features

- **300+ Stock Tickers**: Comprehensive NYSE and NASDAQ coverage
- **Market Data Retrieval**: Automated fetching with proxy support
- **Web Interface**: Filter and search stock data using multiple criteria
- **Auto-Deploy**: Git pull + build + SFTP push in one command
- **Standalone**: Market manager runs independently from deployment

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Two-Step Workflow

**Step 1: Retrieve market data (300+ NYSE & NASDAQ stocks)**
```bash
python3 market_manager.py
```

**Step 2: Deploy to SFTP**
```bash
./deploy.sh
```

### Run Flask App Locally

```bash
python3 App.py
```

Visit `http://localhost:5000` to use the filtering interface.

---

## Command Reference

### 1. Retrieve Stock Data (300+ NYSE & NASDAQ)

```bash
python3 market_manager.py
```

**What it does:**
- ✓ Fetches data for 300+ tickers from NYSE and NASDAQ
- ✓ Saves to `json/stock_data_export.json`
- ✓ Creates automatic backups
- ✓ Proxy rotation support

### 2. Deploy to SFTP

```bash
./deploy.sh
```

**What it does:**
- ✓ Pulls latest code from GitHub
- ✓ Installs dependencies
- ✓ Uploads to SFTP server

**Pre-configured with:**
- Host: `access-5018544625.webspace-host.com`
- User: `a1531117`
- SFTP + SSH (Port 22)

---

## Stock Coverage (300+ Stocks)

### NASDAQ (150+ stocks)
- **Technology**: AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, AMD, INTC, etc.
- **Software & Cloud**: CRM, ORCL, NOW, WDAY, SNOW, PLTR, DOCU, ZM, etc.
- **Semiconductors**: TSM, ASML, NXPI, MRVL, ON, MPWR, QCOM, etc.
- **Biotech**: AMGN, GILD, VRTX, REGN, BIIB, MRNA, BNTX, etc.
- **E-commerce**: EBAY, BKNG, ETSY, MELI, ABNB, DASH, etc.

### NYSE (150+ stocks)
- **Financial Services**: JPM, BAC, WFC, GS, MS, BLK, SCHW, etc.
- **Payment Networks**: V, MA, PYPL, SQ, FIS, FISV, etc.
- **Insurance**: BRK.B, PGR, CB, TRV, ALL, AIG, etc.
- **Healthcare & Pharma**: JNJ, UNH, PFE, ABBV, TMO, CVS, CI, etc.
- **Consumer Goods**: WMT, HD, PG, KO, PEP, COST, NKE, MCD, etc.
- **Energy**: XOM, CVX, COP, SLB, EOG, MPC, PSX, VLO, etc.
- **Industrials**: BA, CAT, GE, MMM, HON, UPS, RTX, LMT, etc.
- **Materials**: LIN, APD, ECL, SHW, DD, NEM, FCX, NUE, etc.
- **REITs**: AMT, PLD, CCI, EQIX, PSA, DLR, SPG, O, etc.
- **Utilities**: NEE, DUK, SO, D, AEP, EXC, SRE, PEG, etc.

---

## Components

### 1. Market Manager (Standalone)

**`market_manager.py`** - Retrieves market data for 300+ stocks

```bash
python3 market_manager.py
```

### 2. SFTP Deployer (Auto Git Pull + Build + Push)

**`sftp_deploy.py`** - Automatically:
- Pulls from git repository
- Installs dependencies
- Uploads to SFTP server

### 3. Deploy Script (SFTP Only)

**`deploy.sh`** - Deploys to SFTP (no market retrieval)

```bash
./deploy.sh                      # Deploy from main
./deploy.sh --branch dev         # Deploy from different branch
./deploy.sh --remote-path /path  # Deploy to different path
```

### 4. Flask Web App

**`App.py`** - Web interface for filtering and exporting stock data

---

## File Structure

```
Reddit-Flask-Issue/
├── App.py                      # Flask web application
├── market_manager.py           # Standalone data retrieval (300+ stocks)
├── market_data_retrieval.py    # Core retrieval logic with proxy support
├── sftp_deploy.py              # Auto git pull + SFTP deployment
├── deploy.sh                   # Main deployment script (SFTP only)
├── requirements.txt            # Python dependencies
├── COMMANDS.md                 # Detailed command reference
├── Templates/
│   └── index.html              # Web interface
└── json/
    ├── stock_data_export.json  # Current market data
    └── backups/                # Timestamped backups
```

---

## Automation

Schedule automated updates with cron:

```bash
# Retrieve market data: Monday-Friday at 6 PM (after market close)
0 18 * * 1-5 cd /path/to/Reddit-Flask-Issue && python3 market_manager.py

# Deploy to SFTP: Monday-Friday at 6:30 PM
30 18 * * 1-5 cd /path/to/Reddit-Flask-Issue && ./deploy.sh
```

Edit crontab:
```bash
crontab -e
```

---

## Documentation

- **[COMMANDS.md](COMMANDS.md)** - Complete command reference with examples
- **[requirements.txt](requirements.txt)** - Python dependencies

---

## Quick Reference

| Task | Command |
|------|---------|
| Retrieve 300+ NYSE/NASDAQ stocks | `python3 market_manager.py` |
| Deploy to SFTP | `./deploy.sh` |
| Run Flask app locally | `python3 App.py` |
| Deploy different branch | `./deploy.sh --branch branch-name` |
| Check data file | `ls -lh json/stock_data_export.json` |

---

## Typical Workflow

```bash
# 1. Retrieve fresh market data
python3 market_manager.py

# 2. Deploy to SFTP server
./deploy.sh
```

Your Flask application with updated market data is now live!
