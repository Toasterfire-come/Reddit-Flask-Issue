#!/bin/bash

###############################################################################
# SFTP Deployment Script
# Deploys to SFTP (auto pull from git + build + push)
#
# Note: Market data retrieval is separate - run market_manager.py manually
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration - SFTP Credentials
SFTP_HOST="access-5018544625.webspace-host.com"
SFTP_PORT=22
SFTP_USER="a1531117"
SFTP_PASS="C2rt3rK#2010"
SFTP_REMOTE_PATH="/"

# Git Configuration
GIT_REPO="https://github.com/Toasterfire-come/Reddit-Flask-Issue.git"
GIT_BRANCH="main"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

###############################################################################
# Functions
###############################################################################

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${GREEN}"
    echo "================================================================================"
    echo "  SFTP Deployment"
    echo "================================================================================"
    echo -e "${NC}"
}

print_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Deploy to SFTP (auto git pull + build + push)

OPTIONS:
    --repo URL          Git repository URL (default: configured repo)
    --branch NAME       Git branch (default: main)
    --remote-path PATH  Remote path on SFTP (default: /)
    -h, --help          Show this help message

EXAMPLES:
    # Deploy from main branch
    $0

    # Deploy from different branch
    $0 --branch dev

    # Deploy to different remote path
    $0 --remote-path /public_html

NOTE:
    To retrieve market data, run separately:
    python3 market_manager.py

EOF
}

deploy_to_sftp() {
    log "Deploying to SFTP"
    echo "================================================================================"

    cd "$SCRIPT_DIR"

    if [ ! -f "sftp_deploy.py" ]; then
        error "sftp_deploy.py not found"
        return 1
    fi

    log "Repository: $GIT_REPO"
    log "Branch: $GIT_BRANCH"
    log "SFTP Host: $SFTP_HOST"
    log "SFTP User: $SFTP_USER"
    log "Remote Path: $SFTP_REMOTE_PATH"
    echo ""

    python3 sftp_deploy.py \
        --repo "$GIT_REPO" \
        --branch "$GIT_BRANCH" \
        --host "$SFTP_HOST" \
        --port "$SFTP_PORT" \
        --user "$SFTP_USER" \
        --password "$SFTP_PASS" \
        --remote-path "$SFTP_REMOTE_PATH"

    if [ $? -eq 0 ]; then
        success "SFTP deployment completed successfully"
        return 0
    else
        error "SFTP deployment failed"
        return 1
    fi
}

###############################################################################
# Main Script
###############################################################################

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --repo)
            GIT_REPO="$2"
            shift 2
            ;;
        --branch)
            GIT_BRANCH="$2"
            shift 2
            ;;
        --remote-path)
            SFTP_REMOTE_PATH="$2"
            shift 2
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Start deployment
print_header

# Check Python
if ! command -v python3 &> /dev/null; then
    error "Python 3 is not installed"
    exit 1
fi

# Deploy to SFTP
deploy_to_sftp || exit 1

# Summary
echo ""
echo -e "${GREEN}"
echo "================================================================================"
echo "  SFTP Deployment Complete!"
echo "================================================================================"
echo -e "${NC}"
echo "✓ Project deployed to SFTP server"
echo "  Host: $SFTP_HOST"
echo "  Path: $SFTP_REMOTE_PATH"
echo ""
echo "To retrieve market data, run:"
echo "  python3 market_manager.py"
echo ""
exit 0
