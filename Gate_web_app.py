from flask import Flask, app, render_template, request, json, url_for
import requests
from werkzeug.utils import redirect


URL1 = "http://localhost:8000"

#Flask app configuration
app = Flask(__name__)


#Endpoints
#Gate Page ##########################################################
@app.route("/",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        r = requests.post(URL1+"/gateslogin",data={'id': request.form['id'],
                                                  'secret': request.form['secret']})
        if r.ok:
            if r.text == "SUCSSESS":
                return redirect(url_for('.gate_page', id = request.form['id']))
            elif r.text == "FAILED":
                return render_template("gateLogin.html", message = "ID or secret wrong, please try again")
        else:
            return "ERROR",r.status_code
    else:
        return render_template("gateLogin.html")

@app.route("/gate/<id>",methods=['GET', 'POST'])
def gate_page(id):
    return render_template("gate.html", id = id)

@app.route("/sendkey",methods=['POST'])
def send_key():    
    r = requests.post(URL1+"/gates", data = {'id': request.form['id'], 
                                             'code': request.form['code'],
                                             's_id': request.form['s_id']})
    if r.ok:
        if r.text == "SUCSSESS":
            return json.jsonify("SUCSSESS")
        else:
            return json.jsonify("FAIL")
    else:
        return r.status_code

#########################################################################
#Starts database and flask web server
if __name__ == "__main__":
    #Find out how you which id and secret is provided
    app.run(host='0.0.0.0', port=8003, debug=True)