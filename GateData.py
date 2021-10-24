from datetime import datetime
from flask import Flask, app, request, render_template, json
import os
from flask_sqlalchemy import SQLAlchemy
import random
import string
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GateData.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.abspath("files")

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

#GateData operations
@app.route("/insertGate",methods=['POST'])
def insert_gate():
    new_gate = GateData(request.form['id'],
                        request.form['secret'],
                        request.form['location'])
    db.session.add(new_gate)
    db.session.commit()
    return 0

@app.route("/queryGate",methods=['GET', 'POST'])
def query_gate():
    if request.method == 'GET':
        return GateData.query.all()
    else:
        gate_id = request.form['id']
        return GateData.query.filter_by(_id = gate_id).first()

@app.route("/deleteGate",methods=['POST'])
def delete_gate():
    gate_id = request.form['id']
    GateData.query.filter_by(_id = gate_id).delete()
    return "Gate "+ gate_id + "has been removed"

#KeyData operations
@app.route("/insertKey",methods=['POST'])
def insert_key():
    new_key = KeyData(request.form['key'])
    db.session.add(new_key)
    db.session.commit()
    return 0

@app.route("/queryKey",methods=['GET','POST'])
def query_key():
    if request.method == 'GET':
        return GateData.query.all()
    else:
        key = request.form['key']
        return GateData.query.filter_by(key = key).first()

@app.route("/deleteKey",methods=['POST'])
def delete_key():
    key = request.form['key']
    KeyData.query.filter_by(key = key).delete()
    return "FAIL"

if __name__ ==  "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=9000, debug=True)