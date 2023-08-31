import argparse
import requests
import time
from datetime import datetime

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Send requests for a specified duration starting at a given time")
parser.add_argument("-u", "--url", required=True, help="URL to send requests to")
parser.add_argument("-c", "--count", required=True, type=int, help="Number of requests per second")
parser.add_argument("-t", "--time", required=True, help="Start time in the format '31/8/2023-20:23:36'")
parser.add_argument("-s", "--seconds", required=True, type=int, help="Duration in seconds")
args = parser.parse_args()

# Convert the provided start time to a datetime object
start_time = datetime.strptime(args.time, "%d/%m/%Y-%H:%M:%S")

# Calculate the time to wait before sending requests
current_time = datetime.now()
time_to_wait = (start_time - current_time).total_seconds()

if time_to_wait > 0:
    print(f"Waiting {time_to_wait:.2f} seconds until the specified start time.")
    time.sleep(time_to_wait)

# Calculate end time
end_time = time.time() + args.seconds

# Send requests for the specified duration
while time.time() < end_time:
    for _ in range(args.count):
        response = requests.get(args.url)
        print(f"Response status code: {response.status_code}")
    
    # Sleep for 1 second
    time.sleep(1)

    # Print a separator line between each second's requests
    print("=" * 30)

print("Request sending complete.")
