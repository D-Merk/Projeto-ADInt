import requests

URL = "http://localhost:8000/users"

if __name__ == "__main__":
    print("Contacting server...")
    r = requests.get(URL)
    print("Code recieved")
    print(">>> " + r.text + " <<<")
    print("Please type the code in the gate")