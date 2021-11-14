from dataclasses import dataclass
from datetime import datetime
from flask import Flask, app, request, render_template, json
import os
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GateData2.sqlite'
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

@dataclass 
class KeyData(db.Model):
    __tablename__ = "key_data"
    _id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String)
    creationtime = db.Column(db.DateTime)

    def __init__(self, key):
        self.key = key
        self.creationtime = datetime.now()

@dataclass
class EntranceData(db.Model):
    __tablename__ = "entrance_data"
    _id = db.Column(db.Integer, primary_key = True)
    gate_id = db.Column(db.Integer)
    entrance_time = db.Column(db.DateTime)
    status = db.Column(db.String)

    def __init__(self, gate_id, entrance_time, status):
        self.gate_id = gate_id
        self.entrance_time = entrance_time
        self.status = status
    




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
            return "Gate Registered"
        except:
            db.session.rollback()
            return "Error in gate registration, try again later",470
        
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
    if KeyData.query.filter_by(key = request.form['key']).first() is None:
        db.session.add(new_key)
        try:
            db.session.commit()
            return "Key inserted"
        except:
            db.session.rollback()
            return "Couldn't inserted key in database",470
    else:
        return "Key already in database",469
        
    

@app.route("/queryKey",methods=['GET','POST'])
def query_key():
    if request.method == 'GET':
        key_query = KeyData.query.all()
        if key_query == None:
            return json.jsonify(["None", ])
        else:
            return json.jsonify([[key_query.key, key_query.creationtime] for gate in key_query])
    else:
        key = request.form['key']
        key_query = KeyData.query.filter_by(key = key).first()
        if key_query == None:
            return json.jsonify(["None", ])
        else:
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
    if gate_query is None:
        return "No such gate exits",469
    gate_query.activations = GateData.activations + 1
    try:
        db.session.commit()
        return "activations updated"
    except:
        db.session.rollback()
        return "Error updating activation",470
    

#EntranceData operations
@app.route("/insertEntrance",methods=['POST'])
def insert_entrance():
    e_time = request.form['time']
    e_time = datetime.strptime(e_time,"%Y-%m-%d %H:%M:%S.%f")
    new_entrance = EntranceData(request.form['id'],
                                e_time,
                                request.form['status'])
    db.session.add(new_entrance)
    try:
        db.session.commit()
        return "entrace inserted"
    except:
        db.session.rollback()
        return "Error - entrance not inserted",469

@app.route("/queryEntrance",methods=['GET','POST'])
def query_entrance():
    if request.method == 'GET':
        entrance_query = EntranceData.query.all()
        return json.jsonify([[entrance.gate_id, entrance.entrance_time, entrance.status] for entrance in entrance_query])
    else:
        gate_id = request.form['id']
        entrance_query = EntranceData.query.filterby(gate_id = gate_id).all()
        return json.jsonify([[entrance.gate_id, entrance.entrance_time, entrance.status] for entrance in entrance_query])


    


if __name__ ==  "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=9003, debug=True)