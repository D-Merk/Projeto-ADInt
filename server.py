from datetime import datetime
from flask import Flask, app, request, render_template, json
import os
from flask_sqlalchemy import SQLAlchemy
import random
import string

#Flask app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GateData.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.abspath("files")

#Database configuration
db = SQLAlchemy(app)

#Database Table
class GateData(db.Model):
    __tablename__ = "gate_data"
    _id = db.Column(db.Integer, primary_key = True)
    secret = db.Column(db.String)
    location = db.Column(db.String)
    activations = db.Column(db.Integer)

    def __init__(self, id, secret, location):
        self._id = id
        self.secret = secret
        self.location = location
        self.activations = 0
    def activate(self):
        self.activations += self.activations
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
class KeyData(db.Model):
    __tablename__ = "key_data"
    _id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String)
    creationtime = db.Column(db.DateTime)

    def __init__(self, key):
        self.key = key
        self.creationtime = datetime.now()
    def insert(self):
        db.session.add(self)
        db.session.commit()





def getKey():
    return ''.join(random.choices(string.ascii_lowercase+string.digits,k=6))

#Endpoints
#Admin Web Page ##########################################################
@app.route("/admin",methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        new_gate = GateData(id=request.form.get("id"), 
                            secret="ABC123", 
                            location=request.form.get("location"))
        new_gate.insert()
    return render_template("admin.html")
@app.route("/register")
def register_gate():
    return render_template("register.html")
@app.route("/list")
def list_gates():
    return render_template("list.html", gates = GateData.query.all())
#########################################################################

@app.route("/gates",methods = ['POST'])
def gates():
    key = request.form['code']
    key_query = KeyData.query.filter_by(key = key).first()
    
    if key_query is None:
        return "FAILED"
    else:
        endtime = datetime.now()
        delta = endtime - key_query.creationtime
        delta = delta.total_seconds()
        print("delta = ",delta)
        if delta > 60:
            #remove from DB
            return "FAIL"
        else:
            return "SUCSSESS"


@app.route("/gateslogin",methods=['POST'])
def gates_login():
    gate_id, gate_secret = request.form['id'], request.form['secret']
    gate_query = GateData.query.filter_by( _id = gate_id).first()
    if gate_secret == gate_query.secret:
        return "SUCSSESS"
    else:
        return "FAILED"

@app.route("/users")
def users():
    key = getKey()
    new_key = KeyData(key)
    new_key.insert()
    return key

#Starts database and flask web server
if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
