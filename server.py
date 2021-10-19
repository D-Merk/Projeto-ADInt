from flask import Flask, app, request, render_template, json
import os
from flask_sqlalchemy import SQLAlchemy

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
    gates = GateData.query.all()
    return render_template("list.html", gates = gates)
#########################################################################

@app.route("/gates")
def gates():
    return "Gates page not implemented"

@app.route("/users")
def users():
    return "Users page not implemented"

#Starts database and flask web server
if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
