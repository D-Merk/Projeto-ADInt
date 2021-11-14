from requests_oauthlib import OAuth2Session
from flask import Flask, app, request, render_template, json, session, redirect, url_for
import requests
import os

#URL for GateData
URL1 = "http://localhost:8000"
#URL for UserData
URL2 = "http://localhost:8002"
#URL for UserData2
URL3 = "http://localhost:9001"

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
    if 'oauth_token' in session:
        login_auth = OAuth2Session(client_id, token=session['oauth_token'])
        ist_id = login_auth.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person').json()
    else:
        return redirect(url_for('.login'))
    r = requests.post(URL1+"/users",data={'s_id': ist_id['username']})
    if r.ok:
        secret = r.text
        return render_template("qrcode.html", secret = secret)
    else:
        return r.status_code

@app.route("/history")
def history_gates():
    if 'oauth_token' in session:
        login_auth = OAuth2Session(client_id, token=session['oauth_token'])
        ist_id = login_auth.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person').json()
    else:
        return redirect(url_for('.login'))
    r = requests.post(URL2+"/queryEntry", data= {'id':ist_id['username']})
    if r.ok:
        accesses = json.loads(r.text)
        return render_template("history.html", accesses = accesses, id = ist_id['username'])
    else:
        r1 = requests.post(URL3+"/queryEntry", data={'id':ist_id['username']})
        if r1.ok:
            accesses = json.loads(r.text)
            return render_template("history.html", accesses = accesses, id = ist_id['username'])
        else:
            return r1.status_code

#########################################################################
#Starts database and flask web server
if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=8001, debug=True)