import string
import requests
from flask import Flask, request
import uuid
import json
from datetime import *
import time
import random
import os

app = Flask("QSM HealthCheck")
global running
running = False

file = {"name": "test"}

@app.route("/")
def index():
    secret_key = request.args.get('secret_key')
    data = request.json
    return "Hello world with " + request.method + " method"


# ================================================CHECK================================================== #

# ------------------------------------------------POST-------------------------------------------------- #
@app.route("/check", methods=["POST"])
def check_add():
    try:
        inp = request.json
        name = inp["name"]
    except:
        return "Invalid input", 405

    print("a")
    stuff = 0

    absolute_path = os.path.dirname(os.path.abspath("database.json")) + "\database.json"

    #with open(absolute_path, "r+") as file:
    stuff = json.dumps(file)

    print("pass")

    last_ping = datetime.today().isoformat("T", "seconds")
    last_ping_timestamp = time.time()
    secret_key = str(''.join(random.choices(string.ascii_letters, k=10)))
    id_u = str(uuid.uuid1())

    stuff[id_u] = {
        "name": name, "status": "ok", "period": 60, "grace": 300, "emails": [], "webhook": None,
        "last_ping": last_ping, "last_ping_timestamp": last_ping_timestamp,
        "secret_key": secret_key
    }

    file.write(json.dump(stuff, indent=4))

    data = {
        "id": id_u,
        "name": name,
        "last_ping": last_ping,
        "last_ping_timestamp": last_ping_timestamp,
        "status": "ok",
        "secret_key": secret_key
    }

    return data


# ------------------------------------------------GET-------------------------------------------------- #
@app.route("/check/<checkID>", methods=["GET"])
def check_show(checkID):
    with open("database.json", "r") as file:
        try:
            x = json.loads(str(file))
            data = x[checkID]
            return data
        except:
            return "Check not found", 404


# ------------------------------------------------DELETE-------------------------------------------------- #
@app.route("/check/<checkID>", methods=["DELETE"])
def check_delete(checkID):
    with open("database.json", "a+") as file:
        x = json.loads(str(file))
        try:
            key = request.args
            if key == x[checkID]["secret_key"]:
                del x[checkID]
                json.dump(x, file)
                return "Check deleted"
            else:
                return "SecretKey for the specified Check is either incorrect or was not provided at all.", 401
        except:
            return "SecretKey for the specified Check is either incorrect or was not provided at all.", 401


# ------------------------------------------------PUT-------------------------------------------------- #
@app.route("/check/<checkID>/setName", methods=["PUT"])
def check_update(checkID):
    key = request.args
    x = request.json
    try:
        name = x["name"]
    except:
        return "Validation exception", 405

    with open("database.json", "a+") as file:
        y = json.loads(str(file))

        if key != y[checkID] or key == '':
            return "SecretKey for the specified Check is either incorrect or was not provided at all.", 401

        try:
            y[checkID]["name"] = name
            json.dump(y, file)

            data = {
                "id": checkID,
                "name": name,
                "last_ping": y[checkID]["last_ping"],
                "last_ping_timestamp": y[checkID]["last_ping_timestamp"],
                "status": y[checkID]["status"]
            }

            return data

        except:
            return "Check not found", 404


# ================================================NOTIFICATION_SETTINGS================================================== #

# ------------------------------------------------GET-------------------------------------------------- #
@app.route("/notification_settings/<checkID>", methods=["GET"])
def notification_show(checkID):
    key = request.args

    with open("database.json", "a+") as file:
        x = json.loads(str(file))

        if key != x[checkID] or key == '':
            return "SecretKey for the specified Check is either incorrect or was not provided at all.", 401

        try:
            data = {"id": checkID, "webhook": x[checkID]["webhook"], "emails": x[checkID]["emails"]}
        except:
            return "Check not found", 404

    return data


# ------------------------------------------------PUT-------------------------------------------------- #
@app.route("/notification_settings/<checkID>", methods=["PUT"])
def notification_update(checkID):
    key = request.args

    with open("database.json", "a+") as file:
        r = request.json
        x = json.loads(str(file))

        if key != x[checkID] or key == '':
            return "SecretKey for the specified Check is either incorrect or was not provided at all.", 401

        try:
            r1 = r["webhook"]
            r2 = r["email"]
        except:
            return "Validation exception", 405

        try:
            x[checkID]["webhook"] = r1
            x[checkID]["emails"] = r2
            json.dump(x, file)
            return notification_show(checkID)
        except:
            return "Check not found", 404


# ================================================SCHEDULE================================================== #

# ------------------------------------------------GET-------------------------------------------------- #
@app.route("/schedule/<checkID>", methods=["GET"])
def schedule_show(checkID):
    key = request.args

    with open("database.json", "a+") as file:
        x = json.loads(str(file))
        try:
            if key != x[checkID] or key == '':
                return "SecretKey for the specified Check is either incorrect or was not provided at all.", 401

            data = {"id": x[checkID]["id"], "period": x[checkID]["period"], "grace": x[checkID]["grace"]}
            return data
        except:
            return "Check not found", 404


# ------------------------------------------------PUT-------------------------------------------------- #
@app.route("/schedule/<checkID>", methods=["PUT"])
def schedule_update(checkID):
    key = request.args

    with open("database.json", "a+") as file:
        r = request.json
        x = json.loads(str(file))

        if key != x[checkID] or key == '':
            return "SecretKey for the specified Check is either incorrect or was not provided at all.", 401

        try:
            r1 = r["id"]
            r2 = r["period"]
            r3 = r["grace"]
        except:
            return "Validation exception", 405

        try:
            x[checkID]["id"] = r1
            x[checkID]["period"] = r2
            x[checkID]["grace"] = r3
            json.dump(x, file)
            return schedule_show(checkID)
        except:
            return "Check not found", 404


# ================================================PING================================================== #

# ------------------------------------------------GET-------------------------------------------------- #
@app.route("/ping/<checkID>", methods=["GET"])
def ping(checkID):
    with open("database.json", "a+") as file:
        x = json.loads(str(file))
        try:
            x[checkID]["last_ping"] = datetime.today().isoformat("T", "seconds")
            json.dump(x, file)
            return "Successful operation"
        except:
            return "check not found", 404


# ================================================CRON================================================== #

# ------------------------------------------------GET-------------------------------------------------- #
@app.route("/cron", methods=["GET"])
def cron():
    if not running:
        notification_count = 0
        running = True
        with open("database.json", "a+") as file:
            x = json.loads(str(file))

            for y in x:
                diff_time = int(datetime.now() - datetime.fromtimestamp(y['timestamp']))

                if diff_time < y["period"]:
                    if y["status"] == "late":
                        notification_count += 1
                        notif = {"status": "ok"}
                        requests.post(y["webhook"], json=notif)
                    y["status"] = "ok"

                if y["period"] < diff_time < (y["period"] + y["grace"]):
                    y["status"] = "grace"

                if diff_time > (y["period"] + y["grace"]):
                    notification_count += 1
                    notif = {"status": "late"}
                    requests.post(y["webhook"], json=notif)
                    y["status"] = "late"

        running = False

    return "During this run " + str(notification_count) + " notifications were sent."
