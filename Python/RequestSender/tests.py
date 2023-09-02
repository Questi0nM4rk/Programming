import shutil
import os
import json
import sqlite3

PATH = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google",
                    "Chrome", "User Data", "Default", "Network", "Cookies")

DESTPATH = os.path.join(os.getcwd(), "Cookies_copy.db")



def main():
    if not os.path.exists(PATH):
        print("Database was not found...")
        return

    shutil.copy(PATH, DESTPATH)

    connection = sqlite3.connect(DESTPATH)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM cookies")
    
    cookies = [dict(row) for row in cursor.fetchall()]
    
    with open('cookies.json', 'w') as json_file:
        json.dump(cookies, json_file, indent=4)

    connection.close()

if __name__ == "__main__":
    main()