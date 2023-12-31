import argparse
import requests
import requests.cookies
from datetime import datetime, timedelta
import time
import json

from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
from os import getenv

load_dotenv()
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

LOGIN_URL = getenv("LOGIN_URL")

class RUN(Enum):                # used primarly for testing
    VISIBLE = True
    NOT_VISIBLE = False


class Cookie():
    domain: str
    expiry: int
    httpOnly: bool
    name: str
    path: str
    sameSite: str
    secure: bool
    value: str
    
    def __init__(self, domain, expiry, httpOnly, name, path,
                 sameSite, secure, value) -> None:
        
        self.domain = domain
        self.expiry = expiry
        self.httpOnly = httpOnly
        self.name = name
        self.path = path
        self.sameSite = sameSite
        self.secure = secure
        self.value = value
        
        
    def is_expired(self) -> bool:
        the_date = datetime.utcfromtimestamp(self.expiry)
        
        return datetime.now() > the_date
    
    
    def to_cookiejar(self) -> requests.cookies.RequestsCookieJar:
        cookie_jar = requests.cookies.RequestsCookieJar()
        
        cookie = requests.cookies.create_cookie(
            domain=self.domain,
            name=self.name,
            value=self.value,
            path=self.path,
            secure=self.secure,
            expires=self.expiry
        )
        
        cookie_jar.set_cookie(cookie)
        
        return cookie_jar
    
    
    @classmethod
    def from_dict(cls, cookie_dict: dict) -> "Cookie":
        return cls(
            cookie_dict["domain"],
            cookie_dict["expiry"],
            cookie_dict["httpOnly"],
            cookie_dict["name"],
            cookie_dict["path"],
            cookie_dict["sameSite"],
            cookie_dict["secure"],
            cookie_dict["value"]
        )
        

class Client:
    cookies: list[Cookie]
    
    start_time: datetime
    end_time: datetime
    time_to_wait: float
    
    
    def __init__(self) -> None:
        self.cookies = []
        
    
    def send_requests(self, url, when: datetime, count, seconds) -> None:
        
        self.start_time = when
        self.end_time = self.start_time + timedelta(seconds=seconds)
        
        current_time = datetime.now()
        time_to_wait = (self.start_time - current_time).total_seconds()
        time_to_wait -= 2

        if time_to_wait > 0:
            print(f"Waiting {time_to_wait:.2f} seconds until the specified start time.")
            time.sleep(time_to_wait)
        
        print(self.start_time)
        print(self.end_time)
        
        while datetime.now() < self.start_time:
            time.sleep(0.2)
        
        while datetime.now() <= self.end_time:
            if self.cookies:
                for _ in range(count):
                    response = requests.get(url, cookies=self.cookies[0].to_cookiejar())
                    print(response.status_code)
            
            time.sleep(1)


class Chrome:

    def __init__(self, run: RUN) -> None:

        if run is RUN.NOT_VISIBLE:
            self.chrome_options = Options()
            self.chrome_options.add_argument("--headless")
            if self.chrome_options:
                self.driver = webdriver.Chrome(options=self.chrome_options)
            
        else:
            self.chrome_options = None
            self.driver = webdriver.Chrome()
            
        self.client = Client()
        
        
    def login(self, url, username, password) -> None:
        
        cookie_data = {}
        with open("secret.json", "r") as f:
            cookie_data = json.load(f)
            
        print(cookie_data)
            
        if cookie_data:
            
            cookie = Cookie.from_dict(cookie_data[0])
            
            if not cookie.is_expired():
                self.client.cookies.append(cookie)
                return
         
        
        self.driver.get(url)
        
        username_field = self.driver.find_element(By.NAME, "credential_0")        
        password_field = self.driver.find_element(By.NAME, "credential_1")        
        submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        submit_button.click()
        
        cookie_dict = self.driver.get_cookies()
        
        self.client.cookies.append(Cookie.from_dict(cookie_dict[0]))
        
        with open("secret.json", "w") as f:
            json.dump(cookie_dict, f, indent=4)
        
        self.driver.quit()
        
    
    def send_request(self, url, count, time, seconds) -> None:
        
        try:
            when = datetime.strptime(time, "%d/%m/%Y-%H:%M:%S")
        
        except:
            try:
                current_date = datetime.now().date()
                hold = datetime.strptime(time, "%H:%M:%S")
                when = datetime.combine(current_date, hold.time())
                
            except:
                return
        
        if seconds > 20 or count > 50:
            return
        
        self.client.send_requests(url, when, count, seconds)
        
        
              
def main():
    try:
        
        parser = argparse.ArgumentParser(description="Send requests for a specified duration starting at a given time")
        parser.add_argument("-u", "--url", required=True, help="URL to send requests to")
        parser.add_argument("-c", "--count", required=True, type=int, help="Number of requests per second")
        parser.add_argument("-t", "--time", required=True, help="Start time in the format '31/8/2023-20:23:36'")
        parser.add_argument("-s", "--seconds", required=True, type=int, help="Duration in seconds")
        args = parser.parse_args()
        
        google = Chrome(RUN.NOT_VISIBLE)
        
        #current_time = datetime.now() + timedelta(seconds=10)
        #time_string = current_time.strftime("%H:%M:%S")
        
        google.login(LOGIN_URL, USERNAME, PASSWORD)
        #google.send_request("http://127.0.0.1:5000", 2, time_string, 2)
        google.send_request(args.url, args.count, args.time, args.seconds)
        
    except Exception as e:
        print(e)
        input()
    


if __name__ == "__main__":
    main()
