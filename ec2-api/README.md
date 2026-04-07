# Hosted skill API (EC2)

FastAPI service that loads the SEO Master skill bundle from `skill/` and exposes `POST /v1/seo` to licensed customers via `X-API-Key`.

## Layout

- `app/` — application code
- `skill/` — full SEO Master bundle (`SKILL.md` + reference `.md` files; committed in this private repo)
- `deploy/` — systemd and nginx examples

## Deploy on Amazon Linux / Ubuntu (EC2)

Example host IP: `18.222.163.42` (use your Elastic IP or DNS name).

1. **Security group:** allow inbound TCP 22 (SSH) and 80/443 (HTTP/S) as needed.

2. **On the server:**

   ```bash
   sudo mkdir -p /opt/hosted-skill-api
   sudo chown $USER:$USER /opt/hosted-skill-api
   ```

   Copy this `ec2-api` folder to `/opt/hosted-skill-api/ec2-api` (rsync, git clone, or CI).

3. **Python venv and dependencies:**

   ```bash
   cd /opt/hosted-skill-api/ec2-api
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Environment:**

   ```bash
   cp .env.example .env
   nano .env   # set ANTHROPIC_API_KEY and API_KEYS
   ```

5. **Skill content:** ships with `git clone` / `git pull` under `skill/`. Override files there if you need a custom prompt, then restart the service.

6. **systemd** (adjust `User`/`paths` if needed):

   ```bash
   sudo cp deploy/systemd/hosted-skill-api.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now hosted-skill-api
   sudo systemctl status hosted-skill-api
   ```

7. **nginx** (optional, for port 80 → app):

   ```bash
   sudo apt install -y nginx   # or yum install nginx
   sudo cp deploy/nginx/hosted-skill-api.conf.example /etc/nginx/sites-available/hosted-skill-api
   # symlink into sites-enabled, test, reload
   ```

## Local run

```bash
cd ec2-api
python3 -m venv .venv && source .venv/bin/activate
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

- Do not expose uvicorn directly to the internet without a reverse proxy and firewall rules.
- Prefer HTTPS (certbot) and restrict `/docs` in production if you do not want public schema discovery.
