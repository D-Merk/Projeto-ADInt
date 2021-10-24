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
    #How to show this shit
    return render_template("list.html", gates = r)#####<-------------------
#########################################################################

@app.route("/gates",methods = ['POST'])
def gates():
    key = request.form['code']
    #Check query
    r = requests.post(URL+"/queryKey", data={'key': key})
    #Check the format of this
    
    if r. is None:
        return "FAILED"
    else:
        endtime = datetime.now()
        delta = endtime - key_query.creationtime
        delta = delta.total_seconds()
        print("delta = ",delta)
        if delta > 60:
            #check delete with REST
            KeyData.query.filter_by(key = key).delete()
            db.session.commit()
            return "FAIL"
        else:
            return "SUCSSESS"


@app.route("/gateslogin",methods=['POST'])
def gates_login():
    gate_id, gate_secret = request.form['id'], request.form['secret']
    #query
    r = requests.post(URL+"/queryKey", data={'id': gate_id})
    #Check the format
    if gate_secret == gate_query.secret:
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
