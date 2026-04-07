# SEO Master API

AI-powered SEO audits via a single command.

## Quick start (for customers)

**1. Install** (one line — needs `curl` and `jq`):

```bash
curl -s https://awsec2.tail0fdcca.ts.net/install > seo && chmod +x seo
```

**2. Set your key:**

```bash
export SEO_API_KEY=your-key-here
```

**3. Use it:**

```bash
# Audit a live website
./seo "Audit example.com for SEO issues"

# Audit your local project directory (Next.js, Nuxt, SvelteKit, Astro, HTML, etc.)
./seo "Full SEO audit" --dir .

# Audit a specific folder
./seo "Check meta tags and structured data" --dir /path/to/my-project

# Pass raw HTML or code as context
./seo "Check this page" --context "<html><head><title>My Page</title></head></html>"

# Pipe a live page in
curl -s https://example.com | ./seo "Audit this HTML"
```

The `--dir` flag auto-detects your framework and collects layout files, metadata, robots.txt, sitemap, config, and SEO components — then sends them to the API for a full source-code audit.

**Supported frameworks:** Next.js (App/Pages Router), Nuxt, SvelteKit, Astro, Vite, static HTML.

That's it. No signup, no SDK, no dependencies beyond `curl` and `jq`.

---

## Server setup (admin only)

FastAPI service that loads the SEO Master skill bundle from `skill/` and exposes `POST /v1/seo` to licensed customers via `X-API-Key`.

## Python version

Use a **stable Python 3.14.x** release (see `requires-python` in `pyproject.toml`). Install 3.14 from your OS or [python.org](https://www.python.org/downloads/), then create the venv with that interpreter:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -c "import sys; assert sys.version_info[:2] == (3, 14), 'Need Python 3.14.x'"
pip install -r requirements.txt
```

If `python3.14` is missing, install Python 3.14 (stable) for your OS, then retry.

## Layout

- `app/` — application code
- `skill/` — full SEO Master bundle (`SKILL.md` + reference `.md` files; committed in this private repo)
- `deploy/` — systemd unit, nginx HTTPS config, setup + cert-renewal scripts

## Deploy on Amazon Linux / Ubuntu (EC2)

Example host IP: `18.222.163.42` (use your Elastic IP or DNS name).

1. **Security group:** allow inbound TCP 22 (SSH) and 80/443 (HTTP/S) as needed.

2. **On the server:**

   ```bash
   sudo mkdir -p /opt/hosted-skill-api
   sudo chown $USER:$USER /opt/hosted-skill-api
   ```

   Copy this `ec2-api` folder to `/opt/hosted-skill-api/ec2-api` (rsync, git clone, or CI).

3. **Python venv and dependencies** (Python **3.14.x**):

   ```bash
   cd /opt/hosted-skill-api/ec2-api
   python3.14 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Environment:**

   ```bash
   cp .env.example .env
   nano .env   # set ANTHROPIC_API_KEY and API_KEYS
   ```

5. **Skill content:** ships with `git clone` / `git pull` under `skill/`. Override files there if you need a custom prompt, then restart the service.

6. **HTTPS + systemd + nginx (one command):**

   Enable HTTPS in your Tailscale admin console (DNS → Enable HTTPS), then:

   ```bash
   sudo bash deploy/setup-https.sh
   ```

   This installs nginx, generates Tailscale TLS certs, configures the reverse proxy (443 → localhost:8000), installs the systemd unit, and starts everything.

   Verify: `curl -s https://awsec2.tail0fdcca.ts.net/health`

7. **Cert renewal** (Tailscale certs expire ~90 days):

   ```bash
   sudo bash deploy/renew-certs.sh
   ```

   Or add a monthly cron:

   ```bash
   echo "0 3 1 * * root /opt/hosted-skill-api/ec2-api/deploy/renew-certs.sh" | sudo tee /etc/cron.d/tailscale-cert-renew
   ```

## Local run

```bash
cd ec2-api
python3.14 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API

- `GET /health` — no auth (for load balancers)
- `POST /v1/seo` — header `X-API-Key: <one of API_KEYS>`, JSON body:

  ```json
  { "message": "Audit example.com for title tags", "context": null }
  ```

OpenAPI docs: `GET /docs` when the service is running.

## Security notes

- Uvicorn binds to `127.0.0.1` only; nginx terminates TLS and proxies.
- HTTPS uses Tailscale-issued certs (`*.ts.net`), valid only for Tailscale peers.
- Restrict `/docs` in production: uncomment the block in the nginx config to return 404.
- Use long random `API_KEYS` for customers, not placeholder strings.
