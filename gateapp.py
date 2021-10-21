import requests
import time
import sys

URL = "http://localhost:8000/gateslogin"
URL1 = "http://localhost:8000/gates"

if __name__ == "__main__":
    myobj = {'id': sys.argv[1],
             'secret': sys.argv[2]}
    r = requests.post(URL, data = myobj)
    print("Contacting Server for...")
    if r.text == "SUCSSESS" :
        print("Secret is valid")
        c = "FAIL"
        while c == "FAIL":
            print("Type the user code :")
            code = input()
            post_info = {'code': code}
            r = requests.post(URL1, data = post_info)
            c = r.text
            print("Contacting Server for...")
            if c == "FAIL":
                print("!!! Code Not valid !!!\n\n")
            else:
                print("!!! Code valid !!!")
                print("!!! The gate will close in 5 s !!!")
                time.sleep(5)
                c = "FAIL"

    else :
        print("The secret is not valid for this gate")
        print("Exiting...")
        exit()