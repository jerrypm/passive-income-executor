#!/bin/bash
# Solana Staking Setup Script
# Prerequisites: solana CLI installed
# WARNING: This manages real crypto. Double-check everything before sending funds.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"
LOG_FILE="$SCRIPT_DIR/staking.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_solana() {
    if ! command -v solana &>/dev/null; then
        echo "Solana CLI not found. Install with:"
        echo '  sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"'
        echo '  export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"'
        exit 1
    fi
    echo "Solana CLI: $(solana --version)"
}

create_wallet() {
    KEYPAIR_PATH="$SCRIPT_DIR/solana-keypair.json"

    if [ -f "$KEYPAIR_PATH" ]; then
        echo "Wallet already exists at $KEYPAIR_PATH"
        solana address -k "$KEYPAIR_PATH"
        return
    fi

    echo "Creating new Solana wallet..."
    solana-keygen new --outfile "$KEYPAIR_PATH" --no-bip39-passphrase

    ADDRESS=$(solana address -k "$KEYPAIR_PATH")
    log "Solana wallet created: $ADDRESS"

    # Save to .env
    echo "" >> "$ENV_FILE"
    echo "# Solana" >> "$ENV_FILE"
    echo "SOLANA_KEYPAIR=$KEYPAIR_PATH" >> "$ENV_FILE"
    echo "SOLANA_ADDRESS=$ADDRESS" >> "$ENV_FILE"

    echo ""
    echo "Wallet address: $ADDRESS"
    echo "Keypair saved to: $KEYPAIR_PATH"
    echo "IMPORTANT: Back up $KEYPAIR_PATH securely!"
}

check_balance() {
    KEYPAIR_PATH="$SCRIPT_DIR/solana-keypair.json"
    if [ ! -f "$KEYPAIR_PATH" ]; then
        echo "No wallet found. Run: $0 create-wallet"
        exit 1
    fi

    solana config set --url https://api.mainnet-beta.solana.com --keypair "$KEYPAIR_PATH" 2>/dev/null
    BALANCE=$(solana balance -k "$KEYPAIR_PATH" 2>/dev/null || echo "0 SOL")
    echo "Balance: $BALANCE"
    log "Balance check: $BALANCE"
}

list_validators() {
    echo "Top validators by stake (mainnet):"
    solana validators --url https://api.mainnet-beta.solana.com 2>/dev/null | head -20
}

stake_sol() {
    KEYPAIR_PATH="$SCRIPT_DIR/solana-keypair.json"
    AMOUNT=${1:-"all"}
    VALIDATOR=${2:-""}

    if [ -z "$VALIDATOR" ]; then
        echo "Usage: $0 stake <amount_SOL> <validator_address>"
        echo ""
        echo "Find validators at: https://www.validators.app/"
        echo "Or run: $0 list-validators"
        exit 1
    fi

    echo "Creating stake account..."
    STAKE_KEYPAIR="$SCRIPT_DIR/solana-stake-$(date +%s).json"
    solana-keygen new --outfile "$STAKE_KEYPAIR" --no-bip39-passphrase --silent

    echo "Staking $AMOUNT SOL to validator $VALIDATOR..."
    solana create-stake-account "$STAKE_KEYPAIR" "$AMOUNT" --keypair "$KEYPAIR_PATH"
    solana delegate-stake "$STAKE_KEYPAIR" "$VALIDATOR" --keypair "$KEYPAIR_PATH"

    log "Staked $AMOUNT SOL to $VALIDATOR (stake account: $STAKE_KEYPAIR)"
    echo ""
    echo "Stake delegated! It will activate in the next epoch (~2-3 days)."
    echo "Check status: solana stake-account $STAKE_KEYPAIR"
}

check_rewards() {
    KEYPAIR_PATH="$SCRIPT_DIR/solana-keypair.json"
    ADDRESS=$(solana address -k "$KEYPAIR_PATH" 2>/dev/null)
    echo "Checking staking rewards for $ADDRESS..."
    solana stakes "$ADDRESS" --url https://api.mainnet-beta.solana.com 2>/dev/null
}

# Main
case "${1:-help}" in
    check)        check_solana ;;
    create-wallet) check_solana && create_wallet ;;
    balance)      check_solana && check_balance ;;
    list-validators) check_solana && list_validators ;;
    stake)        check_solana && stake_sol "$2" "$3" ;;
    rewards)      check_solana && check_rewards ;;
    help|*)
        echo "Solana Staking Helper"
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Commands:"
        echo "  check            Check Solana CLI installation"
        echo "  create-wallet    Create new Solana wallet"
        echo "  balance          Check wallet balance"
        echo "  list-validators  Show top validators"
        echo "  stake <amt> <v>  Stake SOL to validator"
        echo "  rewards          Check staking rewards"
        ;;
esac
