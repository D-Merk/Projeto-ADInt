from datetime import datetime
from flask import Flask, app, request, render_template, json
import os
from flask_sqlalchemy import SQLAlchemy
import random
import string
import requests


#URL for GateData
URL = "http://localhost:9000"

#Flask app configuration
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.abspath("files")

def getKey():
    return ''.join(random.choices(string.ascii_lowercase+string.digits,k=6))

#Endpoints
#Admin Web Page ##########################################################
@app.route("/",methods=['GET','POST'])
@app.route("/admin",methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        new_gate = {'id': request.form.get("id"),
                    'secret':"ABC123",
                    'location':request.form.get("location")}
        r = requests.post(URL+"/insertGate", data=new_gate)
        #Check response to see if id is already registered
    return render_template("admin.html")

@app.route("/register")
def register_gate():
    return render_template("register.html")

@app.route("/list")
def list_gates():
    r = requests.get(URL+"/queryGate")
    gates = json.loads(r.text)
    return render_template("list.html", gates = gates)
#########################################################################

@app.route("/gates",methods = ['POST'])
def gates():
    key = request.form['code']
    #Check query
    r = requests.post(URL+"/queryKey", data={'key': key})
    keys = json.loads(r.text)
    endtime = datetime.now()
    delta = endtime - datetime.strptime(keys[1],"%a, %d %b %Y %H:%M:%S %Z")
    return str(delta.total_seconds())
    
    if keys is None:
        return "FAILED"
    else:
        print(keys[1])
        endtime = datetime.now()
        #delta = endtime - keys[1]
        #print(delta)
        #delta = delta.total_seconds()
        #print("delta = ",delta)
        #if delta > 60:
            #check delete with REST
           # r = requests.post(URL+"/deleteKey", data={'key':keys[0]})
            #return "FAIL"
        #else:
            #return "SUCSSESS"

    return "SUCSSESS"


@app.route("/gateslogin",methods=['POST'])
def gates_login():
    gate_id, gate_secret = request.form['id'], request.form['secret']
    #query
    r = requests.post(URL+"/queryGate", data={'id': gate_id})
    gate = json.loads(r.text)
    #Check the format
    if gate_secret == gate[1]:
        return "SUCSSESS"
    else:
        return "FAILED"

@app.route("/users")
def users():
    key = getKey()
    r = requests.post(URL+"/insertKey", data={'key': key})
    return key

#Starts database and flask web server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
