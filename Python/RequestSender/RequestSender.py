import argparse
import requests
import time
from datetime import datetime
from selenium import webdriver


class cookie:
    name: str
    value: str

    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value
        
    
class bot:
    cookies: list[cookie]
    url: str
    time: str
    end_time: int
    count: int
    seconds: int

    
    def __init__(self, url, time, count, seconds) -> None:
        self.url = url
        self.time = time
        self.count = count
        self.seconds = seconds
        self.end_time
    
    
    def cookies_to_dict(self):
        cookies_dict = {}
        for cookie in self.cookies:
            cookies_dict[cookie.name] = cookie.value
        return cookies_dict    
    
    
    def get_cookies(self):
        # Create a new Chrome browser instance
        driver = webdriver.Chrome()  # Replace with the path to your chromedriver executable

        # Navigate to the website and log in manually
        driver.get('https://muni.islogin.cz/login/-dkNKkBh2fmbeAwUJOEKNfhG?lang=en')

        input()

        # After manually logging in, you can retrieve the cookies
        cookies = driver.get_cookies()
        for cookie in cookies:
            print(f"Cookie Name: {cookie['name']}")
            print(f"Cookie Value: {cookie['value']}")

        # Close the browser
        driver.quit()
        
    
    def send_requests(self):
        # Convert the provided start time to a datetime object
        start_time = datetime.strptime(self.time, "%d/%m/%Y-%H:%M:%S")

        # Calculate the time to wait before sending requests
        current_time = datetime.now()
        time_to_wait = (start_time - current_time).total_seconds()

        if time_to_wait > 0:
            print(f"Waiting {time_to_wait:.2f} seconds until the specified start time.")
            time.sleep(time_to_wait)

        # Calculate end time
        end_time = time.time() + self.seconds

        # Send requests for the specified duration
        while time.time() < end_time:
            for _ in range(self.count):
                #response = requests.get(self.url, cookies=self.cookies_to_dict())
                #print(f"Response status code: {response.status_code}")
                print("Request sent!")
            
            # Sleep for 1 second
            time.sleep(1)


    def parser(self):
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
        self.end_time = time.time() + args.seconds

    def send(self):
        # Send requests for the specified duration
        while time.time() < self.end_time:
            for _ in range(self.count):
                response = requests.get(self.url)
                print(f"Response status code: {response.status_code}")
            
            # Sleep for 1 second
            time.sleep(1)

            # Print a separator line between each second's requests
            print("=" * 30)

        print("Request sending complete.")


def main():
    pass


if __name__ == "__main__":
    main()

