from requests.api import get
from requests_oauthlib import OAuth2Session
from flask import Flask, app, request, render_template, json, session, redirect, url_for
import requests
import random
import os

from Gate_web_app import URL1

URL = "http://localhost:9000"
URL1 = "http://localhost:9003"

app = Flask(__name__)
client_id = "851490151334151"
client_secret = "HvwLdw3qD8DNcbHEaj/neaNZesgBDe1WHdTlu+Z9AYN+GSaq/jFqKSQxspwwx0MVbmah5pQWaDQT4ebXP5Jgdw=="
authorization_base_url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog'
token_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

def get_secret():
    return format(random.randint(0000,9999), '04d')

#Admin Web Page ##########################################################
@app.route("/",methods=['GET','POST'])
def login():
    login_auth = OAuth2Session(client_id, redirect_uri="http://localhost:8005/callback")
    authorization_url, state = login_auth.authorization_url(authorization_base_url)

    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    login_auth = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri = "http://localhost:8005/callback")
    token = login_auth.fetch_token(token_url, client_secret=client_secret,
                                    authorization_response=request.url)
    session['oauth_token'] = token
    return redirect(url_for('.admin_page'))


@app.route("/admin",methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        new_secret = get_secret()
        new_gate = {'id': request.form.get("id"),
                    'secret': new_secret,
                    'location':request.form.get("location")}
        r = requests.post(URL+"/insertGate", data=new_gate)
        r1 = requests.post(URL1+"/insertGate",data=new_gate)
        if r.ok or r1.ok:
            return render_template("secret.html", secret = new_gate["secret"], id = new_gate["id"])
        elif r.ok:
            return r.text,r.status_code
        else:
            return r1.text,r.status_code

    else:
        if 'oauth_token' in session:
            login_auth = OAuth2Session(client_id, token=session['oauth_token'])
            ist_id = login_auth.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person').json()
        #Check response to see if id is already registered
            return render_template("admin.html")
        else:
            return redirect(url_for('.login'))

@app.route("/register")
def register_gate():
    return render_template("register.html")

@app.route("/list")
def list_gates():
    r = requests.get(URL+"/queryGate")
    if r.ok:
        gates = json.loads(r.text)
        return render_template("list.html", gates = gates)
    else:
        r1 = requests.get(URL1+"/queryGate")
        if r1.ok:
            gates = json.loads(r.text)
            return render_template("list.html", gates = gates)
        else:
            return r1.status_code

@app.route("/listAccess")
def list_access():
    r = requests.get(URL+"/queryEntrance")
    if r.ok:
        entrances = json.loads(r.text)
        return render_template("listAccess.html", entrances = entrances)
    else:
        r1 = requests.get(URL1+"/queryEntrance")
        if r1.ok:
            gates = json.loads(r.text)
            return render_template("list.html", gates = gates)
        else:
            return r1.status_code
#########################################################################

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=8005, debug=True)