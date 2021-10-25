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

def get_secret():
    return format(random.randint(0000,9999), '04d')

#Endpoints
#Admin Web Page ##########################################################
@app.route("/",methods=['GET','POST'])
@app.route("/admin",methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        new_gate = {'id': request.form.get("id"),
                    'secret': get_secret(),
                    'location':request.form.get("location")}
        r = requests.post(URL+"/insertGate", data=new_gate)
        if r.status_code == 469:
            return r.text,469
        else:
            return render_template("secret.html", secret = new_gate["secret"], id = new_gate["id"])
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
    gate_id = request.form['id']
    #Check query
    r = requests.post(URL+"/queryKey", data={'key': key})
    keys = json.loads(r.text)
    endtime = datetime.now()
    
    if keys is None:
        return "FAIL"
    else:
        endtime = datetime.now()
        delta = endtime - datetime.strptime(keys[1],"%a, %d %b %Y %H:%M:%S %Z")
        delta = delta.total_seconds()
        if delta > 60:
            r = requests.post(URL+"/deleteKey", data={'key':keys[0]})
            return "FAIL"
        else:
            r = requests.post(URL+"/updateAct", data={'id': gate_id})
            r = requests.post(URL+"/deleteKey", data={'key':keys[0]})
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
