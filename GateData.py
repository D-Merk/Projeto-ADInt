from dataclasses import dataclass
from datetime import datetime
from flask import Flask, app, request, render_template, json
import os
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GateData.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.abspath("files")

db = SQLAlchemy(app)

#Database Table
@dataclass
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

@dataclass 
class KeyData(db.Model):
    __tablename__ = "key_data"
    _id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String)
    creationtime = db.Column(db.DateTime)

    def __init__(self, key):
        self.key = key
        self.creationtime = datetime.now()

#GateData operations
@app.route("/insertGate",methods=['POST'])
def insert_gate():
    new_gate = GateData(request.form['id'],
                        request.form['secret'],
                        request.form['location'])
    if GateData.query.filter_by(_id = new_gate._id).first() is None:
        db.session.add(new_gate)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return "Gate Registered"
    else:
        return "Gate with that id is already registered",469

@app.route("/queryGate",methods=['GET', 'POST'])
def query_gate():
    if request.method == 'GET':
        gate_query = GateData.query.all()
        return json.jsonify([[gate._id, gate.secret, gate.location, gate.activations] for gate in gate_query])
    else:
        gate_id = request.form['id']
        gate_query = GateData.query.filter_by(_id = gate_id).first()
        return json.jsonify([gate_query._id, gate_query.secret, gate_query.location, gate_query.activations])

@app.route("/deleteGate",methods=['POST'])
def delete_gate():
    gate_id = request.form['id']
    GateData.query.filter_by(_id = gate_id).delete()
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return "Gate deleted"

#KeyData operations
@app.route("/insertKey",methods=['POST'])
def insert_key():
    new_key = KeyData(request.form['key'])
    db.session.add(new_key)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return "Key inserted"

@app.route("/queryKey",methods=['GET','POST'])
def query_key():
    if request.method == 'GET':
        key_query = KeyData.query.all()
        return json.jsonify([[key_query.key, key_query.creationtime] for gate in key_query])
    else:
        key = request.form['key']
        key_query = KeyData.query.filter_by(key = key).first()
        return json.jsonify([key_query.key, key_query.creationtime])

@app.route("/deleteKey",methods=['POST'])
def delete_key():
    key = request.form['key']
    KeyData.query.filter_by(key = key).delete()
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return "Key deleted"

@app.route("/updateAct",methods=['POST'])
def update_act():
    gate_id = request.form['id']
    gate_query = GateData.query.filter_by(_id = gate_id).first()
    gate_query.activations = GateData.activations + 1
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return "activations updated"

if __name__ ==  "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=9000, debug=True)