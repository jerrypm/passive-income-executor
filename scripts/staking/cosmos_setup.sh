#!/bin/bash
# Cosmos (ATOM) Staking Setup Script
# Prerequisites: gaiad CLI installed
# WARNING: This manages real crypto. Double-check everything before sending funds.

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
ENV_FILE="$PROJECT_DIR/.env"
LOG_FILE="$PROJECT_DIR/logs/staking.log"
CHAIN_ID="cosmoshub-4"
NODE="https://cosmos-rpc.publicnode.com:443"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_gaiad() {
    if ! command -v gaiad &>/dev/null; then
        echo "gaiad not found. Install with:"
        echo "  git clone https://github.com/cosmos/gaia.git"
        echo "  cd gaia && make install"
        echo ""
        echo "Or via Go:"
        echo "  go install github.com/cosmos/gaia/v18/cmd/gaiad@latest"
        exit 1
    fi
    echo "gaiad: $(gaiad version 2>/dev/null || echo 'installed')"
}

create_wallet() {
    KEYNAME="passive-income"

    # Check if key already exists
    if gaiad keys show "$KEYNAME" 2>/dev/null; then
        echo "Wallet '$KEYNAME' already exists"
        gaiad keys show "$KEYNAME" -a
        return
    fi

    echo "Creating new Cosmos wallet '$KEYNAME'..."
    echo "IMPORTANT: Write down the mnemonic phrase!"
    echo ""

    gaiad keys add "$KEYNAME"

    ADDRESS=$(gaiad keys show "$KEYNAME" -a)
    log "Cosmos wallet created: $ADDRESS"

    # Save address to .env
    echo "" >> "$ENV_FILE"
    echo "# Cosmos" >> "$ENV_FILE"
    echo "COSMOS_KEY_NAME=$KEYNAME" >> "$ENV_FILE"
    echo "COSMOS_ADDRESS=$ADDRESS" >> "$ENV_FILE"

    echo ""
    echo "Wallet address: $ADDRESS"
    echo "Key name: $KEYNAME"
    echo "IMPORTANT: Back up your mnemonic phrase securely!"
}

check_balance() {
    KEYNAME="passive-income"
    ADDRESS=$(gaiad keys show "$KEYNAME" -a 2>/dev/null || echo "")

    if [ -z "$ADDRESS" ]; then
        echo "No wallet found. Run: $0 create-wallet"
        exit 1
    fi

    echo "Address: $ADDRESS"
    gaiad query bank balances "$ADDRESS" --node "$NODE" 2>/dev/null || echo "Could not query balance"
}

list_validators() {
    echo "Top validators on Cosmos Hub:"
    gaiad query staking validators --node "$NODE" --limit 20 --output json 2>/dev/null | \
        python3 -c "
import json, sys
data = json.load(sys.stdin)
for v in sorted(data.get('validators',[]), key=lambda x: int(x.get('tokens','0')), reverse=True)[:15]:
    tokens = int(v.get('tokens','0')) / 1e6
    rate = float(v.get('commission',{}).get('commission_rates',{}).get('rate','0'))
    print(f\"  {v['description']['moniker'][:30]:<30} | {tokens:>12,.0f} ATOM | {rate*100:.1f}% commission\")
" 2>/dev/null || echo "Could not fetch validators. Check network connection."
}

stake_atom() {
    KEYNAME="passive-income"
    AMOUNT=${1:-""}
    VALIDATOR=${2:-""}

    if [ -z "$AMOUNT" ] || [ -z "$VALIDATOR" ]; then
        echo "Usage: $0 stake <amount_uatom> <validator_address>"
        echo ""
        echo "Example: $0 stake 1000000 cosmosvaloper1..."
        echo "(1000000 uatom = 1 ATOM)"
        echo ""
        echo "Find validators: $0 list-validators"
        exit 1
    fi

    echo "Delegating ${AMOUNT} uatom to validator $VALIDATOR..."
    gaiad tx staking delegate "$VALIDATOR" "${AMOUNT}uatom" \
        --from "$KEYNAME" \
        --chain-id "$CHAIN_ID" \
        --node "$NODE" \
        --gas auto \
        --gas-adjustment 1.5 \
        --gas-prices 0.025uatom

    log "Delegated ${AMOUNT} uatom to $VALIDATOR"
}

check_rewards() {
    KEYNAME="passive-income"
    ADDRESS=$(gaiad keys show "$KEYNAME" -a 2>/dev/null || echo "")

    if [ -z "$ADDRESS" ]; then
        echo "No wallet found."
        exit 1
    fi

    echo "Staking rewards for $ADDRESS:"
    gaiad query distribution rewards "$ADDRESS" --node "$NODE" 2>/dev/null || echo "Could not query rewards"
}

claim_rewards() {
    KEYNAME="passive-income"

    echo "Claiming all staking rewards..."
    gaiad tx distribution withdraw-all-rewards \
        --from "$KEYNAME" \
        --chain-id "$CHAIN_ID" \
        --node "$NODE" \
        --gas auto \
        --gas-adjustment 1.5 \
        --gas-prices 0.025uatom

    log "Claimed all staking rewards"
}

# Main
case "${1:-help}" in
    check)            check_gaiad ;;
    create-wallet)    check_gaiad && create_wallet ;;
    balance)          check_gaiad && check_balance ;;
    list-validators)  check_gaiad && list_validators ;;
    stake)            check_gaiad && stake_atom "$2" "$3" ;;
    rewards)          check_gaiad && check_rewards ;;
    claim)            check_gaiad && claim_rewards ;;
    help|*)
        echo "Cosmos (ATOM) Staking Helper"
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Commands:"
        echo "  check            Check gaiad CLI installation"
        echo "  create-wallet    Create new Cosmos wallet"
        echo "  balance          Check wallet balance"
        echo "  list-validators  Show top validators"
        echo "  stake <amt> <v>  Delegate ATOM to validator"
        echo "  rewards          Check staking rewards"
        echo "  claim            Claim all rewards"
        ;;
esac
