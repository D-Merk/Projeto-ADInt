from requests_oauthlib import OAuth2Session
from flask import Flask, app, request, render_template, json, session, redirect, url_for
import requests
import os

#URL for GateData
URL1 = "http://localhost:8000"
#URL for UserData
URL2 = "http://localhost:8002"

#Flask app configuration
app = Flask(__name__)

#Fenixc auth
client_id = "851490151334150"
client_secret = "Xle/1mFtLI4/K+9RxgmrB6Yo+CsCxAXZER34QtDBVgrukHx2vxf/nTcaGYpvHKHCmPCnQFEvYiVIAIUknTM6xg=="
authorization_base_url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog'
token_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'



#Endpoints
#User Web Page ##########################################################
@app.route("/",methods=['GET','POST'])
def login():
    login_auth = OAuth2Session(client_id, redirect_uri = "http://localhost:8001/callback")
    authorization_url, state = login_auth.authorization_url(authorization_base_url)

    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/callback",methods=['GET'])
def callback():
    login_auth = OAuth2Session(client_id, state=session['oauth_state'],redirect_uri="http://localhost:8001/callback")
    token = login_auth.fetch_token(token_url, client_secret=client_secret,
                                    authorization_response=request.url)
    session['oauth_token'] = token
    return redirect(url_for('.user_page'))

@app.route("/user",methods=['GET', 'POST'])
def user_page():
    login_auth = OAuth2Session(client_id, token=session['oauth_token'])
    ist_id = login_auth.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person').json()
    return render_template("user.html",id = ist_id['username'])

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
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=8001, debug=True)