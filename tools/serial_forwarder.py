#!/usr/bin/env python3
"""
Simple serial -> HTTP forwarder for Arduino (reads JSON lines from serial and posts them to Django endpoint).

Usage (Windows example):
python tools/serial_forwarder.py --port COM3 --baud 9600 --url http://127.0.0.1:8000/rest/arduino/

Dependencies:
pip install pyserial requests

The Arduino sketch should print a single JSON object per line, for example:
{"serial":"ARDUINO1","valor":23.45,"humedad":45.2}

This script will parse each line as JSON. If it contains a "serial" and "valor" field it will POST to the URL provided.
"""

import argparse
import json
import logging
import time
import requests
import serial
from serial.serialutil import SerialException

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
LOG = logging.getLogger('serial_forwarder')

DEFAULT_BAUD = 9600
DEFAULT_TIMEOUT = 2.0
RECONNECT_DELAY = 2.0


def forward_loop(port: str, baud: int, url: str):
    LOG.info('Opening serial port %s @ %d', port, baud)

    while True:
        try:
            with serial.Serial(port, baud, timeout=DEFAULT_TIMEOUT) as ser:
                LOG.info('Serial port opened: %s', ser.name)
                # give Arduino a moment to boot if necessary
                time.sleep(1.0)

                while True:
                    try:
                        line = ser.readline()
                    except SerialException as se:
                        LOG.error('Serial read error: %s', se)
                        break

                    if not line:
                        # timeout with no data
                        continue

                    try:
                        text = line.decode('utf-8', errors='ignore').strip()
                    except Exception:
                        LOG.warning('Could not decode serial line; skipping')
                        continue

                    if not text:
                        continue

                    LOG.debug('Line from serial: %s', text)

                    # Try to find JSON in the line
                    data = None
                    try:
                        data = json.loads(text)
                    except json.JSONDecodeError:
                        # If not plain JSON, attempt to extract a JSON substring
                        # (robust for extra debug prints around JSON)
                        try:
                            start = text.find('{')
                            end = text.rfind('}')
                            if start != -1 and end != -1 and end > start:
                                payload = text[start:end+1]
                                data = json.loads(payload)
                        except Exception:
                            data = None

                    if not isinstance(data, dict):
                        LOG.debug('No JSON payload in line; skipping: %s', text)
                        continue

                    # validate fields we care about
                    if 'serial' not in data or 'valor' not in data:
                        LOG.warning('JSON missing required fields (serial/valor). Skipping: %s', data)
                        continue

                    # Prepare body and send
                    body = {'serial': data['serial'], 'valor': float(data['valor'])}
                    # Optionally include humidity if present
                    if 'humedad' in data:
                        body['humedad'] = float(data['humedad'])

                    try:
                        LOG.info('POST -> %s  payload=%s', url, body)
                        r = requests.post(url, json=body, timeout=5)
                        LOG.info('Response: %d %s', r.status_code, r.text.strip())
                    except Exception as exc:
                        LOG.error('Failed to POST to %s: %s', url, exc)

        except SerialException as e:
            LOG.error('Failed to open serial port %s: %s', port, e)

        LOG.info('Retrying serial port in %0.1f seconds...', RECONNECT_DELAY)
        time.sleep(RECONNECT_DELAY)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Forward JSON lines from serial to HTTP endpoint')
    parser.add_argument('--port', required=True, help='Serial port name (e.g., COM3 or /dev/ttyUSB0)')
    parser.add_argument('--baud', type=int, default=DEFAULT_BAUD, help='Baud rate (default 9600)')
    parser.add_argument('--url', required=True, help='Full URL of the endpoint (e.g. http://127.0.0.1:8000/rest/arduino/)')

    args = parser.parse_args()

    try:
        forward_loop(args.port, args.baud, args.url)
    except KeyboardInterrupt:
        LOG.info('Stopped by user')
