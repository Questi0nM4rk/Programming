import argparse
import requests
import time
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Cookie:
    name: str
    value: str

    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value
        
    
class Bot:
    cookies: list[Cookie]
    url: str
    time: str
    end_time: int
    count: int
    seconds: int
    time_to_wait: float

    
    def __init__(self, url, time, count, seconds) -> None:
        self.url = url
        self.time = time
        self.count = count
        self.seconds = seconds
        self.cookies = []
        
        self.get_cookies()
        self.send_requests()
    
    def cookies_to_dict(self):
        cookies_dict = {}
        for cookie in self.cookies:
            cookies_dict[cookie.name] = cookie.value
        return cookies_dict    
    
    
    def get_cookies(self):
        driver = webdriver.Chrome()

        driver.get('https://muni.islogin.cz/login/-dkNKkBh2fmbeAwUJOEKNfhG?lang=en')

        input()
        
        cookies = driver.get_cookies()
        
        for cooki in cookies:
            print(f"Cookie Name: {cooki['name']}")
            print(f"Cookie Value: {cooki['value']}")

            self.cookies.append(Cookie(cooki['name'], cooki['value']))
        
        driver.quit()
        
    
    def send_requests(self):
        
        start_time = datetime.strptime(self.time, "%d/%m/%Y-%H:%M:%S")
        end_time = start_time + timedelta(seconds=self.seconds)

        current_time = datetime.now()
        self.time_to_wait = (start_time - current_time).total_seconds()
        self.time_to_wait -= 2

        if self.time_to_wait > 0:
            print(f"Waiting {self.time_to_wait:.2f} seconds until the specified start time.")
            time.sleep(self.time_to_wait)
        
        print(start_time)
        print(end_time)
        
        while datetime.now() < start_time:
            time.sleep(0.2)
        
        while datetime.now() <= end_time:
            print("while")
            for _ in range(self.count):
                response = requests.get(self.url, cookies=self.cookies_to_dict())
                print(response.content)
            
            time.sleep(1)

    
class Chrome:
    """
    driver
    options
    client    
    """

    def __init__(self, invis: bool, bot: Bot) -> None:

        if invis:
            self.chrome_options = Options().add_argument("--headless")
            if self.chrome_options:
                self.driver = webdriver.Chrome(options=self.chrome_options)
            
        else:
            self.chrome_options = None
            self.driver = webdriver.Chrome()
            
        self.client = bot
        
        
    def login(self, url, username, password):
        self.driver.get(url)
        
        username_field = self.driver.find_element(By.NAME, "credential_0")        
        password_field = self.driver.find_element(By.NAME, "credential_1")        
        submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        submit_button.click()
        
        
        
def main():
    parser = argparse.ArgumentParser(description="Send requests for a specified duration starting at a given time")
    parser.add_argument("-u", "--url", required=True, help="URL to send requests to")
    parser.add_argument("-c", "--count", required=True, type=int, help="Number of requests per second")
    parser.add_argument("-t", "--time", required=True, help="Start time in the format '31/8/2023-20:23:36'")
    parser.add_argument("-s", "--seconds", required=True, type=int, help="Duration in seconds")
    args = parser.parse_args()
    
    bot = Bot(args.url, args.time, args.count, args.seconds)
    


if __name__ == "__main__":
    main()
