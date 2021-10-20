import requests
import time

URL = "http://localhost:8000/gates"

if __name__ == "__main__":

    print("Contacting server...")
    r = requests.get(URL)
    print("Code recieved")
    print(">>> " + r.text + " <<<")