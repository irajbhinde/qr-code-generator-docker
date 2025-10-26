#!/usr/bin/env python3
import argparse
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

try:
    import qrcode
except ImportError:
    print("Missing dependency 'qrcode'. Did you install requirements.txt?", file=sys.stderr)
    sys.exit(1)

DEFAULT_OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/qr_codes")
DEFAULT_LOG_DIR = os.getenv("LOG_DIR", "/app/logs")
DEFAULT_URL = os.getenv("DEFAULT_URL", "http://github.com/kaw393939")

def setup_logging(log_dir: str):
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / "app.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout),
        ]
    )
    return log_path

def generate_qr(url: str, output_dir: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"qr_{ts}.png"
    out_path = Path(output_dir) / filename
    img = qrcode.make(url)
    img.save(out_path)
    return str(out_path)

def parse_args():
    parser = argparse.ArgumentParser(description="Simple QR Code Generator")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL/text to encode into a QR code")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Directory to write QR codes")
    parser.add_argument("--log-dir", default=DEFAULT_LOG_DIR, help="Directory for logs")
    return parser.parse_args()

def main():
    args = parse_args()
    log_path = setup_logging(args.log_dir)
    logging.info("Starting QR Code generation")
    logging.info("Using URL: %s", args.url)
    logging.info("Output dir: %s", args.output_dir)
    try:
        out_file = generate_qr(args.url, args.output_dir)
        logging.info("QR code saved to: %s", out_file)
        print(out_file)  # also print for convenience in docker logs
        return 0
    except Exception as e:
        logging.exception("Failed to generate QR code: %s", e)
        return 2

if __name__ == "__main__":
    sys.exit(main())
