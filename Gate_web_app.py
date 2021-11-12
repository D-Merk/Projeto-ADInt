from flask import Flask, app, render_template, request
import requests

URL1 = "http://localhost:8000"

#Flask app configuration
app = Flask(__name__)


#Endpoints
#Gate Page ##########################################################
@app.route("/",methods=['GET','POST'])
@app.route("/gate",methods=['GET', 'POST'])
def gate_page():
    return render_template("gate.html")

@app.route("/sendkey",methods=['POST'])
def send_key():    
    r = requests.post(URL1+"/gates", data = {'id': request.form['id'], 
                                             'code': request.form['code']})
    if r.text == "SUCSSESS":
        return "SUCSSESS"
    else:
        return "FAIL"

#########################################################################
#Starts database and flask web server
if __name__ == "__main__":
    #Find out how you which id and secret is provided
    app.run(host='0.0.0.0', port=8003, debug=True)