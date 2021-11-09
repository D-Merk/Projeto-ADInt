from flask import Flask, app, request, render_template, json
import requests

#URL for GateData
URL1 = "http://localhost:8000"
#URL for UserData
URL2 = "http://localhost:8002"

#Flask app configuration
app = Flask(__name__)


#Endpoints
#User Web Page ##########################################################
@app.route("/",methods=['GET','POST'])
@app.route("/user",methods=['GET', 'POST'])
def user_page():
    return render_template("user.html")

@app.route("/qrcode")
def new_qrcode():
    r = requests.get(URL1+"/users")
    secret = r.text
    return render_template("qrcode.html", secret = secret)

@app.route("/history")
def history_gates():
    r = requests.post(URL2+"/queryEntry", data= {'id':2})
    accesses = json.loads(r.text)
    return render_template("history.html", accesses = accesses)
#########################################################################
#Starts database and flask web server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)