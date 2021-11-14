from dataclasses import dataclass
from datetime import datetime
from flask import Flask, app, request, json
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserData2.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.abspath("files")

db = SQLAlchemy(app)

@dataclass
class UserData(db.Model):
    __tablename__ = "user_data"
    _id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.String)
    gate_id = db.Column(db.Integer)
    entrance_time = db.Column(db.DateTime)
    status = db.Column(db.String)

    def __init__(self, id, gate_id, entry_time, status):
        self.student_id = id
        self.gate_id = gate_id
        self.entrance_time = entry_time
        self.status = status

@app.route("/insertEntry",methods=['POST'])
def insert_entry():
    e_time = request.form['time']
    e_time = datetime.strptime(e_time,"%Y-%m-%d %H:%M:%S.%f")
    new_entry = UserData(request.form['id'],
                         request.form['gate_id'],
                         e_time,
                         request.form['status'])
    db.session.add(new_entry)
    try:
        db.session.commit()
        return "Entry registered"
    except:
        db.session.rollback()
        return "Error, entry not registered",470

@app.route("/queryEntry", methods=['POST'])
def query_entry():
    id = request.form['id']
    entry_query = UserData.query.filter_by(student_id = id).all()
    return json.jsonify([[entry.gate_id, entry.entrance_time, entry.status] for entry in entry_query])

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=9001, debug=True)