from datetime import datetime
import re
from flask import Flask, app, request, render_template, json
import os
from flask_sqlalchemy import SQLAlchemy
import random
import string
import requests


#URL for GateData
URL = "http://localhost:9000"
URL1 = "http://localhost:8002"
URL2 = "http://localhost:9003"
URL3 = "http://localhost:9001"

#Flask app configuration
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.abspath("files")

def getKey():
    return ''.join(random.choices(string.ascii_lowercase+string.digits,k=6))

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
        r1 = requests.post(URL2+"/insertEntrance",data={'id': gate_id,
                                                          'time': endtime,
                                                          'status': "FAIL"}) 

        r2 = requests.post(URL1+"/insertEntry",data={'id': s_id,
                                                   'gate_id': gate_id,
                                                   'time': endtime,
                                                   'status': "FAIL"})
        r3 = requests.post(URL3+"/insertEntry",data={'id': s_id,
                                                   'gate_id': gate_id,
                                                   'time': endtime,
                                                   'status': "FAIL"})
        if (r.ok or r1.ok) and (r2.ok or r3.ok):
            return "FAIL"
        elif not r.ok:
            return r.text,r.status_code
        elif not r1.ok:
            return r1.text,r1.status_code
        elif not r2.ok:
            return r2.text,r2.status_code
        else:
            return r3.text,r3.status_code


    else:
        endtime = datetime.now()
        delta = endtime - datetime.strptime(keys[1],"%a, %d %b %Y %H:%M:%S %Z")
        delta = delta.total_seconds()
        if delta > 60:
            r = requests.post(URL+"/deleteKey", data={'key':keys[0]})
            if not r.ok:
                return r.status_code
            
            r = requests.post(URL+"/insertEntrance",data={'id': gate_id,
                                                          'time': endtime,
                                                          'status': "FAIL"})
            r1 = requests.post(URL2+"/insertEntrance",data={'id': gate_id,
                                                          'time': endtime,
                                                          'status': "FAIL"})
            
            r2 = requests.post(URL1+"/insertEntry",data={'id': s_id,
                                                       'gate_id': gate_id,
                                                       'time': endtime,
                                                       'status': "FAIL"})
            r3 = requests.post(URL3+"/insertEntry",data={'id': s_id,
                                                       'gate_id': gate_id,
                                                       'time': endtime,
                                                       'status': "FAIL"})
            
            if (r.ok or r1.ok) and (r2.ok or r3.ok):
                return "FAIL"
            elif not r.ok:
                return r.text,r.status_code
            elif not r1.ok:
                return r1.text,r1.status_code
            elif not r2.ok:
                return r2.text,r2.status_code
            else:
                return r3.text,r3.status_code
        else:
            r = requests.post(URL+"/updateAct", data={'id': gate_id})
            r1 = requests.post(URL2+"/updateAct", data={'id': gate_id})

            r2 = requests.post(URL+"/deleteKey", data={'key':keys[0]})
            r3 = requests.post(URL2+"/deleteKey", data={'key':keys[0]})
            
            r4 = requests.post(URL+"/insertEntrance",data={'id': gate_id,
                                                          'time': endtime,
                                                          'status': "SUCSSESS"})
            r5 = requests.post(URL2+"/insertEntrance",data={'id': gate_id,
                                                          'time': endtime,
                                                          'status': "SUCSSESS"})
            
            r6 = requests.post(URL1+"/insertEntry",data={'id': s_id,
                                                        'gate_id': gate_id,
                                                        'time': endtime,
                                                        'status': "SUCSSESS"})
            r7 = requests.post(URL3+"/insertEntry",data={'id': s_id,
                                                        'gate_id': gate_id,
                                                        'time': endtime,
                                                        'status': "SUCSSESS"})
            if(r.ok or r1.ok) and (r2.ok or r3.ok) and (r4.ok or r5.ok) and (r6.ok or r7.ok):
                return "SUCSSESS"
            
            

@app.route("/gateslogin",methods=['POST'])
def gates_login():
    gate_id, gate_secret = request.form['id'], request.form['secret']
    #query
    r = requests.post(URL+"/queryGate", data={'id': gate_id})
    if not r.ok:
        r = requests.post(URL2+"/queryGate")
        if not r.ok:
            return r.status_code
        else:
            gate = json.loads(r.text)
            #Check the format
            if gate_secret == gate[1]:
                return "SUCSSESS"
            else:
                return "FAILED"
    else:
        gate = json.loads(r.text)
        if gate_secret == gate[1]:
            return "SUCSSESS"
        else:
            return "FAILED"

@app.route("/users",methods=['POST'])
def users():
    s_id = request.form['s_id']
    key = getKey()
    r = requests.post(URL+"/insertKey", data={'key': key})
    r1 = requests.post(URL2+"/insertKey",data={'key':key})
    if r.ok or r1.ok:
        key = s_id+"/"+key
        return key
    elif not r.ok:
        return "ERROR",r.status_code
    else:
        return "ERROR2",r1.status_code
        

#Starts database and flask web server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
