#!/usr/bin/env bash
# Renew Tailscale HTTPS certs and reload nginx.
# Run via cron monthly:  0 3 1 * * /opt/hosted-skill-api/ec2-api/deploy/renew-certs.sh
set -euo pipefail

DOMAIN="awsec2.tail0fdcca.ts.net"
CERT_DIR="/etc/tailscale-certs"

tailscale cert \
    --cert-file "$CERT_DIR/$DOMAIN.crt" \
    --key-file  "$CERT_DIR/$DOMAIN.key" \
    "$DOMAIN"
chmod 600 "$CERT_DIR/$DOMAIN.key"
systemctl reload nginx
echo "$(date): Certs renewed for $DOMAIN" >> /var/log/tailscale-cert-renew.log
