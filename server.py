from datetime import datetime
from flask import Flask, app, request, render_template, json
import os
from flask_sqlalchemy import SQLAlchemy
import random
import string
import requests
from requests.sessions import Request


#URL for GateData
URL = "http://localhost:9000"
URL1 = "http://localhost:8002"

#Flask app configuration
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.abspath("files")

def getKey():
    return ''.join(random.choices(string.ascii_lowercase+string.digits,k=6))

def get_secret():
    return format(random.randint(0000,9999), '04d')

#Endpoints
@app.route("/gates",methods = ['POST'])
def gates():
    key = request.form['code']
    gate_id = request.form['id']
    s_id = request.form['s_id']

    #Check query
    r = requests.post(URL+"/queryKey", data={'key': key})
    keys = json.loads(r.text)
    endtime = datetime.now()
    
    if keys[0] == "None":
        r = requests.post(URL+"/insertEntrance",data={'id': gate_id,
                                                          'time': endtime,
                                                          'status': "FAIL"})
        r = requests.post(URL1+"insertEntry",data={'id': s_id,
                                                   'gate_id': gate_id,
                                                   'time': endtime,
                                                   'status': "FAIL"})
        return "FAIL"
    else:
        endtime = datetime.now()
        delta = endtime - datetime.strptime(keys[1],"%a, %d %b %Y %H:%M:%S %Z")
        delta = delta.total_seconds()
        if delta > 60:
            r = requests.post(URL+"/deleteKey", data={'key':keys[0]})
            
            r = requests.post(URL+"/insertEntrance",data={'id': gate_id,
                                                          'time': endtime,
                                                          'status': "FAIL"})
            
            r = requests.post(URL1+"insertEntry",data={'id': s_id,
                                                       'gate_id': gate_id,
                                                       'time': endtime,
                                                       'status': "FAIL"})
            return "FAIL"
        else:
            r = requests.post(URL+"/updateAct", data={'id': gate_id})
            
            r = requests.post(URL+"/deleteKey", data={'key':keys[0]})
            
            r = requests.post(URL+"/insertEntrance",data={'id': gate_id,
                                                          'time': endtime,
                                                          'status': "SUCSSESS"})
            
            r = requests.post(URL1+"insertEntry",data={'id': s_id,
                                                        'gate_id': gate_id,
                                                        'time': endtime,
                                                        'status': "SUCSSESS"})
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
