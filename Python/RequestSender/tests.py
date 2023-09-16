from selenium import webdriver
import requests
from datetime import datetime

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
    count: int
    seconds: int

    
    def __init__(self, url, time, count, seconds) -> None:
        self.url = url
        self.time = time
        self.count = count
        self.seconds = seconds
    
    
    def cookies_to_dict(self):
        cookies_dict = {}
        for cookie in self.cookies:
            cookies_dict[cookie.name] = cookie.value
        return cookies_dict    
    
    
    def get_cookies(self):
        # Create a new Chrome browser instance
        driver = webdriver.Chrome()  # Replace with the path to your chromedriver executable

        # Navigate to the website and log in manually
        driver.get('https://muni.islogin.cz/login/-dkNKkBh2fmbeAwUJOEKNfhG?lang=en')  # Replace with the URL of the website you want to log in to

        input()

        # After manually logging in, you can retrieve the cookies
        cookies = driver.get_cookies()
        for cookie in cookies:
            print(f"Cookie Name: {cookie['name']}")
            print(f"Cookie Value: {cookie['value']}")

        # Close the browser
        driver.quit()
        
    
    def send_request(self, time, ):
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



class IS:
    Bot: bot        
