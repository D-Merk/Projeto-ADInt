from requests_oauthlib import OAuth2Session
from flask import Flask, app, request, render_template, json, session, redirect, url_for
import requests
import os

app = Flask(__name__)
client_id = "851490151334151"
client_secret = "HvwLdw3qD8DNcbHEaj/neaNZesgBDe1WHdTlu+Z9AYN+GSaq/jFqKSQxspwwx0MVbmah5pQWaDQT4ebXP5Jgdw=="
authorization_base_url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog'
token_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

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
        new_gate = {'id': request.form.get("id"),
                    'secret': get_secret(),
                    'location':request.form.get("location")}
        r = requests.post(URL+"/insertGate", data=new_gate)
        if r.status_code == 469:
            return r.text,469
        else:
            return render_template("secret.html", secret = new_gate["secret"], id = new_gate["id"])
        #Check response to see if id is already registered
    return render_template("admin.html")

@app.route("/register")
def register_gate():
    return render_template("register.html")

@app.route("/list")
def list_gates():
    r = requests.get(URL+"/queryGate")
    gates = json.loads(r.text)
    return render_template("list.html", gates = gates)

@app.route("/listAccess")
def list_access():
    r = requests.get(URL+"/queryEntrance")
    entrances = json.loads(r.text)
    return render_template("listAccess.html", entrances = entrances)
#########################################################################

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=8005, debug=True)