#!/usr/bin/env bash
# NovaOS Setup Script
# Installs Ollama (if needed), pulls the default model, and installs Python deps.

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
cat << 'EOF'
  _   _                   ___  ____
 | \ | | _____   ____ _ / _ \/ ___|
 |  \| |/ _ \ \ / / _` | | | \___ \
 | |\  | (_) \ V / (_| | |_| |___) |
 |_| \_|\___/ \_/ \__,_|\___/|____/

  Setup Script
EOF
echo -e "${NC}"

# ---- Check Python version ------------------------------------------------
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED="3.12"
if python3 -c "import sys; exit(0 if sys.version_info >= (3,12) else 1)"; then
    echo -e "${GREEN}✓ Python ${PYTHON_VERSION}${NC}"
else
    echo -e "${RED}✗ Python 3.12+ required. Found: ${PYTHON_VERSION}${NC}"
    exit 1
fi

# ---- Install Ollama -------------------------------------------------------
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama already installed$(ollama --version 2>/dev/null || true)${NC}"
else
    echo -e "${YELLOW}→ Installing Ollama...${NC}"
    curl -fsSL https://ollama.ai/install.sh | sh
    echo -e "${GREEN}✓ Ollama installed${NC}"
fi

# ---- Start Ollama service ------------------------------------------------
if ! pgrep -x "ollama" > /dev/null; then
    echo -e "${YELLOW}→ Starting Ollama service...${NC}"
    ollama serve &>/dev/null &
    sleep 3
fi

# ---- Pull default model --------------------------------------------------
DEFAULT_MODEL="${DEFAULT_MODEL:-llama3.2}"
echo -e "${YELLOW}→ Pulling model: ${DEFAULT_MODEL}${NC}"
ollama pull "${DEFAULT_MODEL}"
echo -e "${GREEN}✓ Model ready: ${DEFAULT_MODEL}${NC}"

# ---- Install Python dependencies -----------------------------------------
echo -e "${YELLOW}→ Installing Python dependencies...${NC}"
pip install --quiet -r requirements.txt
pip install --quiet -e .
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# ---- Copy .env.example ---------------------------------------------------
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env from .env.example${NC}"
fi

echo ""
echo -e "${GREEN}✓ NovaOS is ready!${NC}"
echo ""
echo -e "  Run the dashboard:  ${CYAN}novaos dashboard${NC}"
echo -e "  Interactive chat:   ${CYAN}novaos chat${NC}"
echo -e "  Single command:     ${CYAN}novaos run \"Open Chrome\"${NC}"
echo -e "  Health check:       ${CYAN}novaos doctor${NC}"
echo ""
