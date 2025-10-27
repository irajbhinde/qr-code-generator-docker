# QR Code Generator (Dockerized)

A minimal QR Code generator packaged in a secure, efficient Docker image.

## How it works
- `main.py` reads a `--url` (or `DEFAULT_URL` env var), generates a PNG into `/app/qr_codes`, and logs to `/app/logs/app.log`.
- Defaults are safe, and the container runs as a non-root user.

---

## Step 1: Prerequisites
- Install Docker: [https://www.docker.com/get-started](https://www.docker.com/get-started)
- Create a Docker Hub account: [https://hub.docker.com/](https://hub.docker.com/)
- (Optional) Python 3.12+ if you want to run locally outside Docker

Verify Docker installation:
```powershell
docker --version
```

---

## Step 2: Build & Run Locally

### Build the image
```powershell
docker build -t qr-code-generator-app .
```

### Run (detached)
```powershell
docker run -d --name qr-generator qr-code-generator-app
```

### Run with volume and PowerShell path syntax
This ensures the generated QR codes are visible on your Windows host:
```powershell
mkdir qr_codes -ErrorAction SilentlyContinue
docker run -d --name qr-generator `
  -v "${PWD}\qr_codes:/app/qr_codes" `
  qr-code-generator-app
```

### Override URL and save to host
```powershell
docker run --rm -v "${PWD}\qr_codes:/app/qr_codes" `
  qr-code-generator-app --url https://github.com/irajbhinde
```

### Check logs
```powershell
docker logs qr-generator
```

### Stop & remove container
```powershell
docker stop qr-generator
docker rm qr-generator
```

---

## Step 3: Push to Docker Hub

### Login
```powershell
docker logout
docker login
```

Use your Docker Hub **username** and **access token**.

### Tag & push
```powershell
$env:DH_USER = "rajbhinde"
docker tag qr-code-generator-app $env:DH_USER/qr-code-generator-app:latest
docker push $env:DH_USER/qr-code-generator-app:latest
```

Your Docker Hub repository:  
🔗 [https://hub.docker.com/r/rajbhinde/qr-code-generator-app](https://hub.docker.com/r/rajbhinde/qr-code-generator-app)

---

## Step 4: GitHub Repository Setup

Initialize and push your project to GitHub:
```powershell
git init
git add .
git commit -m "Initial commit of QR Code Generator application"
git branch -M main
git remote add origin https://github.com/irajbhinde/qr-code-generator-docker.git
git push -u origin main
```

---

## Step 5: GitHub Actions (CI/CD Pipeline)

This repository includes a workflow file `.github/workflows/docker-image.yml` that will:
- Build the Docker image on pushes to `main` or on tag creation.
- Login to Docker Hub using GitHub Secrets.
- Tag the image with both `latest` and short Git SHA.
- Push the image to Docker Hub.

### Required Repository Secrets
- `DOCKERHUB_USERNAME` — your Docker Hub username (`rajbhinde`)
- `DOCKERHUB_TOKEN` — your Docker Hub access token with *Read/Write/Delete* scopes.

---

## Environment Variables
| Variable | Default Value | Description |
|-----------|----------------|-------------|
| `DEFAULT_URL` | `https://github.com/irajbhinde` | Default URL encoded in the QR code |
| `OUTPUT_DIR` | `/app/qr_codes` | Directory for PNG outputs |
| `LOG_DIR` | `/app/logs` | Directory for log files |

---

## Screenshots

Included following screenshots :
- ✅ Container logs showing the QR code generation.
- ✅ QR code image visible in local `qr_codes/` folder.
- ✅ GitHub Actions successful run (build & push).

---

## Makefile Shortcuts
For quick commands (PowerShell compatible):
```powershell
make build   # Build image
make run     # Run container
make logs    # Show container logs
make stop    # Stop container
make push DH_USER=rajbhinde  # Push image to Docker Hub
```

---

## Security Notes
- Runs as a **non-root user** for safety.
- Based on **python:3.12-slim-bullseye** for minimal attack surface.
- Uses `--no-cache-dir` during pip install to reduce image size.
- `.dockerignore` excludes unnecessary build context (logs, cache, git files).

---

## Reflection
See `reflection.md` for details on challenges, troubleshooting, and improvements.

---

## Links
- GitHub Repository: [https://github.com/irajbhinde/qr-code-generator-docker](https://github.com/irajbhinde/qr-code-generator-docker)
- Docker Hub Image: [https://hub.docker.com/r/rajbhinde/qr-code-generator-app](https://hub.docker.com/r/rajbhinde/qr-code-generator-app)
