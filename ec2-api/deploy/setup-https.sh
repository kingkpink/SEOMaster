#!/usr/bin/env bash
# Sets up HTTPS for the hosted skill API using Tailscale certs + nginx + systemd.
# Run as root (or with sudo) on the EC2 instance.
#
# Usage:  sudo bash deploy/setup-https.sh
#
# Prerequisites:
#   - Tailscale running and logged in
#   - HTTPS enabled on your tailnet (admin console → DNS → Enable HTTPS)
#   - git pull done so ec2-api/ is current
#   - .env configured with ANTHROPIC_API_KEY and API_KEYS
#   - .venv created with: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

set -euo pipefail

DOMAIN="awsec2.tail0fdcca.ts.net"
CERT_DIR="/etc/tailscale-certs"
API_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NGINX_CONF="/etc/nginx/sites-available/hosted-skill-api"
NGINX_ENABLED="/etc/nginx/sites-enabled/hosted-skill-api"

echo "==> API directory: $API_DIR"

# --- 1. Install nginx if missing ---
if ! command -v nginx &>/dev/null; then
    echo "==> Installing nginx..."
    apt-get update -qq && apt-get install -y -qq nginx
fi

# --- 2. Generate Tailscale TLS certs ---
echo "==> Generating Tailscale certs for $DOMAIN..."
mkdir -p "$CERT_DIR"
tailscale cert \
    --cert-file "$CERT_DIR/$DOMAIN.crt" \
    --key-file  "$CERT_DIR/$DOMAIN.key" \
    "$DOMAIN"
chmod 600 "$CERT_DIR/$DOMAIN.key"
echo "    Certs at $CERT_DIR/$DOMAIN.{crt,key}"

# --- 3. Install nginx config ---
echo "==> Configuring nginx..."
cp "$API_DIR/deploy/nginx/hosted-skill-api.conf.example" "$NGINX_CONF"

# Enable site, remove default if it exists
ln -sf "$NGINX_CONF" "$NGINX_ENABLED"
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl reload nginx
echo "    nginx listening on 80 (redirect) and 443 (TLS)"

# --- 4. Install and start the API systemd unit ---
echo "==> Installing systemd unit..."

# Patch paths in the unit file to match this clone
sed \
    -e "s|WorkingDirectory=.*|WorkingDirectory=$API_DIR|" \
    -e "s|EnvironmentFile=.*|EnvironmentFile=$API_DIR/.env|" \
    -e "s|ExecStart=.*|ExecStart=$API_DIR/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000|" \
    "$API_DIR/deploy/systemd/hosted-skill-api.service" \
    > /etc/systemd/system/hosted-skill-api.service

systemctl daemon-reload
systemctl enable --now hosted-skill-api
echo "    systemd unit enabled and started"

# --- 5. Verify ---
sleep 2
echo ""
echo "==> Checking services..."
systemctl is-active --quiet hosted-skill-api && echo "    [OK] hosted-skill-api is running" || echo "    [FAIL] hosted-skill-api"
curl -sS -m 5 http://127.0.0.1:8000/health && echo "" || echo "    [FAIL] health check"
echo ""
echo "==> Done. Test from your Tailscale network:"
echo "    curl -s https://$DOMAIN/health"
echo ""
echo "==> Tailscale certs expire in ~90 days. Renew with:"
echo "    sudo tailscale cert --cert-file $CERT_DIR/$DOMAIN.crt --key-file $CERT_DIR/$DOMAIN.key $DOMAIN"
echo "    sudo systemctl reload nginx"
