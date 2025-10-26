# Reflection: Dockerizing the QR Code Generator

## What worked well
-

## What was challenging
-

## Security considerations you implemented
- Non-root user (`myuser`)
- Minimal base image (`python:3.12-slim-bullseye`)
- No cache pip installs, `.dockerignore` to reduce context
- Read/write limited to `/app`

## CI/CD
- Describe how the GitHub Actions workflow authenticates to Docker Hub and pushes tags.

## What you'd improve next
- Add unit tests and linting
- Multi-stage build if native deps are introduced
- Automated vulnerability scanning (e.g., `docker scout` or `grype`)
