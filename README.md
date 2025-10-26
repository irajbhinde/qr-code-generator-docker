# QR Code Generator (Dockerized)

A minimal QR Code generator packaged in a secure, efficient Docker image.

## How it works
- `main.py` reads a `--url` (or `DEFAULT_URL` env var), generates a PNG into `/app/qr_codes`, and logs to `/app/logs/app.log`.
- Defaults are safe, and the container runs as a non-root user.

---

## Step 1: Prerequisites
- Install Docker: https://www.docker.com/get-started
- Create a Docker Hub account: https://hub.docker.com/
- (Optional) Python 3.12+ if you want to run locally outside Docker

Verify Docker:
```bash
docker --version
```

## Step 2: Build & Run Locally

Build the image:
```bash
docker build -t qr-code-generator-app .
```

Run (detached):
```bash
docker run -d --name qr-generator qr-code-generator-app
```

Override URL + mount host directory for outputs:
```bash
mkdir -p ./qr_codes
docker run -d --name qr-generator \
  -v $PWD/qr_codes:/app/qr_codes \
  qr-code-generator-app --url https://www.njit.edu
```

Check logs:
```bash
docker logs qr-generator
```

Stop & remove:
```bash
docker stop qr-generator && docker rm qr-generator
```

## Step 3: Push to Docker Hub

Login:
```bash
docker login
```

Tag & push:
```bash
# replace with your Docker Hub username
export DH_USER="your-dockerhub-username"
docker tag qr-code-generator-app $DH_USER/qr-code-generator-app:latest
docker push $DH_USER/qr-code-generator-app:latest
```

## GitHub Repository
Initialize and push:
```bash
git init
git add .
git commit -m "Initial commit of QR Code Generator application"
git branch -M main
git remote add origin https://github.com/your-username/qr-code-generator.git
git push -u origin main
```

## CI: GitHub Actions (Docker -> Docker Hub)
This repo includes `.github/workflows/docker-image.yml` that will:
- build the image on pushes to `main` and on tags,
- login to Docker Hub using repo secrets,
- tag `latest` and the short Git SHA,
- push to your registry.

**Required repo secrets:**
- `DOCKERHUB_USERNAME` — your Docker Hub username
- `DOCKERHUB_TOKEN` — a personal access token or password

## Environment Variables
- `DEFAULT_URL` — default content to encode (default: `http://github.com/kaw393939`)
- `OUTPUT_DIR` — directory for PNGs (default: `/app/qr_codes`)
- `LOG_DIR` — directory for logs (default: `/app/logs`)

## Screenshots to Include (Grading)
1. **Container Logs** — show `docker logs qr-generator` with a successful run (includes a path to the generated PNG).
2. **GitHub Actions** — screenshot of a successful workflow run showing build and push steps.
3. **Docker Hub** — (optional but nice) screenshot of your repository page showing pushed tags.

## Reflection
See `reflection.md` for a template.

---

## Makefile shortcuts
```bash
make build
make run
make logs
make stop
make push DH_USER=your-dockerhub-username
```
