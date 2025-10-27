# Reflection: Dockerizing the QR Code Generator

## What worked well
- Successfully built a lightweight and secure Docker image using `python:3.12-slim-bullseye`.
- The QR Code Generator application ran perfectly inside the container and created valid PNG images.
- Docker Hub integration worked after fixing access token and tagging issues.
- GitHub Actions workflow automatically built and pushed the image to Docker Hub once secrets were configured correctly.
- Running as a non-root user (`myuser`) improved security while maintaining correct file permissions.

---

## Challenges Faced and How They Were Solved

### 1. PowerShell `export` Command Not Recognized
**Issue:**  
When tagging and pushing the Docker image from PowerShell, the terminal threw:
```
The term 'export' is not recognized as the name of a cmdlet...
```

**Cause:**  
`export` is a Unix command and not recognized in Windows PowerShell.

**Fix:**  
Used PowerShell syntax to set environment variables:
```powershell
$env:DH_USER = "rajbhinde"
docker tag qr-code-generator-app $env:DH_USER/qr-code-generator-app:latest
docker push $env:DH_USER/qr-code-generator-app:latest
```
This made the commands compatible with Windows.

---

### 2. GitHub Actions “401 Unauthorized” When Pushing to Docker Hub
**Issue:**  
GitHub Actions workflow failed with:
```
failed to fetch oauth token: 401 Unauthorized: access token has insufficient scopes
```

**Cause:**  
The Docker Hub access token used in GitHub Secrets did not have the correct write permissions.

**Fix:**
1. Generated a new Docker Hub **Access Token** (with *Read, Write, and Delete* permissions) from  
   [https://hub.docker.com/settings/security](https://hub.docker.com/settings/security)
2. Updated the repository **Secrets** in GitHub → *Settings → Secrets and variables → Actions*:
   - `DOCKERHUB_USERNAME = rajbhinde`
   - `DOCKERHUB_TOKEN = <new access token>`
3. Re-ran the workflow, and it successfully pushed the image to Docker Hub.

---

### 3. Empty `qr_codes` Folder on Host
**Issue:**  
After running the container with volume mapping, the local `qr_codes` folder remained empty.

**Cause:**  
PowerShell interprets `$PWD` differently than Linux shells, causing the Docker mount path to break (e.g., creating `qr_codes;C`).

**Fix:**  
Used proper PowerShell path syntax:
```powershell
docker run --rm -v "${PWD}\qr_codes:/app/qr_codes" rajbhinde/qr-code-generator-app
```
This correctly mounted the host folder, and the generated QR code appeared inside `qr_codes/`.

---

### 4. Docker Hub Repository Overview Empty
**Observation:**  
After pushing the image, the Docker Hub page showed “No overview available”.

**Solution:**  
This is optional. A README can be added manually in Docker Hub’s **Manage Repository** section to show project information.

---

## Security Considerations Implemented
- Created and switched to a **non-root user (`myuser`)** to prevent privilege escalation.
- Used the **minimal base image** `python:3.12-slim-bullseye` to reduce the attack surface.
- Disabled Python cache writes and buffering:
  ```dockerfile
  ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
  ```
- Restricted writable directories to `/app/logs` and `/app/qr_codes`.
- Used `--no-cache-dir` in `pip install` for smaller and cleaner layers.
- Excluded unnecessary files with `.dockerignore` to make the image more efficient.

---

## CI/CD and Automation
- GitHub Actions workflow (`.github/workflows/docker-image.yml`) builds and pushes the image to Docker Hub automatically on every push to `main`.
- Docker Hub credentials (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) are stored securely in GitHub Secrets.
- Workflow uses:
  - `docker/login-action` for secure Docker Hub login.
  - `docker/build-push-action` to build and push images for both `amd64` and `arm64` platforms.
- Tags include both `latest` and short Git SHA identifiers for traceability.

---

## What I'd Improve Next
- Add unit tests and include automated testing in the GitHub Actions workflow before building the Docker image.
- Integrate static analysis and vulnerability scanning tools such as `docker scout`, `grype`, or `trivy`.
- Use a multi-stage Docker build if additional dependencies are introduced in the future.
- Automatically sync the project’s `README.md` to the Docker Hub repository for better presentation.

---

## Final Outcome
After overcoming the setup and PowerShell challenges, everything is working perfectly:
- ✅ The Docker image builds successfully without errors.  
- ✅ The container runs correctly and generates QR code PNG files.  
- ✅ The image is publicly available on Docker Hub:  
  🔗 [https://hub.docker.com/r/rajbhinde/qr-code-generator-app](https://hub.docker.com/r/rajbhinde/qr-code-generator-app)  
- ✅ The source code and CI/CD pipeline are hosted on GitHub:  
  🔗 [https://github.com/rajbhinde/qr-code-generator-docker](https://github.com/rajbhinde/qr-code-generator-docker)

Overall, this project was a great hands-on experience in **secure Dockerization, CI/CD automation, and troubleshooting real-world DevOps issues**.
