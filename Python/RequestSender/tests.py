import argparse



# Parse command-line arguments
parser = argparse.ArgumentParser(description="Send requests for a specified duration starting at a given time")
parser.add_argument("-u", "--url", required=True, help="URL to send requests to")
parser.add_argument("-c", "--count", required=True, type=int, help="Number of requests per second")
parser.add_argument("-t", "--time", required=True, help="Start time in the format '31/8/2023-20:23:36'")
parser.add_argument("-s", "--seconds", required=True, type=int, help="Duration in seconds")
args = parser.parse_args()

print("args")
print(args.url)
