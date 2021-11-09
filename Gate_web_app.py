from flask import Flask, app, render_template

#Flask app configuration
app = Flask(__name__)


#Endpoints
#Gate Page ##########################################################
@app.route("/",methods=['GET','POST'])
@app.route("/gate",methods=['GET', 'POST'])
def gate_page():
    return render_template("gate.html")
#########################################################################
#Starts database and flask web server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8003, debug=True)