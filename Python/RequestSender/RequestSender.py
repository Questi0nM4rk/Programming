import argparse
import time
import requests
from datetime import datetime, timedelta

# Function to send requests
def send_requests(url, count):
    for _ in range(count):
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")
        time.sleep(0.9)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Schedule and send requests")
parser.add_argument("-u", "--url", required=True, help="URL to send requests to")
parser.add_argument("-t", "--time", required=True, help="Time in the format '31/8/2023-20:23:36'")
parser.add_argument("-c", "--count", required=True, type=int, help="Number of requests per second")
args = parser.parse_args()

# Convert the provided time to a datetime object
target_time = datetime.strptime(args.time, "%d/%m/%Y-%H:%M:%S")

# Calculate the time to wait before checking for execution
current_time = datetime.now()
time_to_wait = (target_time - current_time).total_seconds() - 5

if time_to_wait > 0:
    print(f"Sleeping {time_to_wait:.2f} seconds before checking for execution.")
    time.sleep(time_to_wait)

# Check if it's time to execute
while datetime.now() < target_time:
    remaining_time = target_time - datetime.now()
    print(f"Waiting {remaining_time.total_seconds():.2f} seconds until the specified time.")
    time.sleep(0.5)

print("Sending requests...")
send_requests(args.url, args.count)
print("Request sending complete.")