# L402 Paywall Setup (Aperture + LND)

## Prerequisites
- LND running (Lightning Network Daemon)
- Go installed
- Ollama running on localhost:11434

## Step 1: Install LND
```bash
# Via Homebrew
brew install lnd

# Or from source
git clone https://github.com/lightningnetwork/lnd.git
cd lnd && make install
```

## Step 2: Configure LND
```bash
mkdir -p ~/.lnd
cat > ~/.lnd/lnd.conf << 'EOF'
[Application Options]
alias=passive-income-node
listen=0.0.0.0:9735
rpclisten=localhost:10009

[Bitcoin]
bitcoin.active=true
bitcoin.mainnet=true
bitcoin.node=neutrino

[Neutrino]
neutrino.connect=btcd-mainnet.lightning.computer
neutrino.connect=faucet.lightning.community
EOF

# Start LND
lnd &
lncli create  # First time: create wallet
```

## Step 3: Install Aperture
```bash
go install github.com/lightninglabs/aperture@latest
```

## Step 4: Configure Aperture
```bash
mkdir -p ~/.aperture
cat > ~/.aperture/aperture.yaml << 'EOF'
listenaddr: "localhost:8081"
staticroot: ""
authenticator:
  lndhost: "localhost:10009"
  tlspath: "~/.lnd/tls.cert"
  macpath: "~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon"
services:
  - name: "ollama-ai"
    hostregexp: "localhost:8081"
    pathregexp: "/api/.*"
    address: "localhost:11434"
    protocol: "https"
    price: 10
    auth_header: "L402"
EOF

# Start Aperture
aperture &
```

## Step 5: Test
```bash
# This will return 402 with Lightning invoice
curl -i http://localhost:8081/api/generate \
  -d '{"model":"llama3","prompt":"hello"}'

# Pay invoice, then use the preimage as auth
curl http://localhost:8081/api/generate \
  -H "Authorization: L402 <macaroon>:<preimage>" \
  -d '{"model":"llama3","prompt":"hello"}'
```

## Notes
- LND requires syncing (can take hours for neutrino mode)
- Aperture handles L402 auth automatically
- Each request costs 10 sats (~$0.001)
- Revenue visible via: `lncli listinvoices`
