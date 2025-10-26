# Use the official Python image from DockerHub as the base image
FROM python:3.12-slim-bullseye

# Security/behavior defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install OS deps (none required for qrcode[pil]) and create non-root user early
RUN useradd -m myuser

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for logs and QR codes, and set ownership to the non-root user
RUN mkdir -p /app/logs /app/qr_codes && chown -R myuser:myuser /app

# Copy the rest of the application’s source code into the container, setting ownership to 'myuser'
COPY --chown=myuser:myuser . .

# Switch to the non-root user for security
USER myuser

# Use ENTRYPOINT and CMD to allow flexibility when running the container
ENTRYPOINT ["python", "main.py"]
CMD ["--url", "http://github.com/irajbhinde"]
