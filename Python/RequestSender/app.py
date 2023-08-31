from flask import Flask
from datetime import datetime


app = Flask("testServer")
req = 0


app.route("/")
def getRequest():
    global req
    req += 1
    date = datetime.now()
    time = date.strftime("%H:%M:%S")
    
        
    print(f"{time} - req: {req}")
    