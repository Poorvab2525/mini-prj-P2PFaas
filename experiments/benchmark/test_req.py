import requests
import time
import mimetypes
import logging
from threading import Thread
from io import BytesIO
from PIL import Image

# Constants
OVERHEAD = 2.366  # Adjusted overhead value
# URL = "http://10.100.12.148:8080/function/pigo-faceblur"
URL = "http://localhost:18080/function/pigo-faceblur"
PAYLOAD = "./blobs/familyr_320p.jpg"
NUM_REQUESTS = 200
TIMEOUT = 30  # seconds
RUN_DURATION = 60  # 2 minutes in seconds
SLEEP_BETWEEN_REQUESTS = 0.1  # seconds

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_binary(file_path):
    """Read binary data from the specified file."""
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

def send_request(session, url, payload, headers):
    """Send a POST request and measure the response time."""
    try:
        start_time = time.time()
        response = session.post(url, data=payload, headers=headers, timeout=TIMEOUT)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000.0
        logging.info(f"Status: {response.status_code}, Time: {elapsed_time:.3f} ms, Adjusted: {elapsed_time - OVERHEAD:.3f} ms")
        return elapsed_time
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def main():
    """Main function to execute the load testing."""
    session = requests.Session()
    payload_bin = read_binary(PAYLOAD)
    payload_mime = mimetypes.guess_type(PAYLOAD)[0] or "application/octet-stream"
    
    if payload_bin is None:
        logging.error("Exiting due to missing payload.")
        return
    
    headers = {'Content-Type': payload_mime, 'Connection': 'Keep-Alive'}
    delays = []
    
    for i in range(NUM_REQUESTS):
        delay = send_request(session, URL, payload_bin, headers)
        if delay is not None:
            delays.append(delay)
        time.sleep(0.1)  # Prevent overwhelming the server
    
    session.close()
    
    if delays:
        avg_delay = sum(delays) / len(delays)
        logging.info(f"\nAverage delay: {avg_delay:.3f} ms")
    else:
        logging.warning("No successful requests. Unable to calculate average delay.")

if __name__ == "__main__":
    main()