"""
app.py
upload contours to s3 with id problem grade IN problems folder
upload full packet images to s3 with id packet grade IN packets folder
"""

# imports
import markowitz
from flask import Flask, request, jsonify,render_template, send_file
from flask_cors import CORS
import sys


# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app)

images = []
img_form = "<img src = '{}'>"

form_params = dict()
#stock_symbols
form_params["LargeG"] = "FSPGX"
form_params["LargeV"] = "^SVX"
form_params["SmallG"] = "^RUT"
form_params["SmallV"] = "^SVX"
form_params["Med"] = "^SP400"
form_params["Inter"] = "VTIAX"
form_params["Emerging"] = "VEMAX"
form_params["InterBond"] = "GVI"
form_params["Long"] = "ILTB"
form_params["Corp"] = "^SPBDACPT"
form_params["Highyield"] = "HYG"
form_params["Muni"] = "MUB"
form_params["Foreignbonds"] = "BNDX"
form_params["Debt"] = "JEDAX"
form_params["Realestate"] = "^DJUSRE"
form_params["V.C."] = "^AMZX"
form_params["Commodities"] = "^DJCI"
form_params["Cash"] = "BIL"
#clientinfo
form_params["name"] = "John Smith"
form_params["birthday"] = "12/28/1960"
form_params["time"] = "7"


# Do machine Learning Autograding.
@app.route("/", methods=["GET", "POST"])
def load_home():
    return render_template('index.html') #"Hello World!":

@app.route("/mark", methods=["GET", "POST"])
def mark():
    global images
    images = []
    risk = request.form.get('risk')
    print(risk)
    risk=int(risk)
    print("RISK_LEVEL :",risk)
    images,portfolios,returns,risks = markowitz.markowitz_run(risk_level=risk)
    vals=dict()
    html_images = [img_form.format(i) for i in images]

    line = markowitz.line()
    line7 = markowitz.line(7)
    html_img = img_form.format(line)
    html_img7 = img_form.format(line7)
    html_images.append(html_img)
    html_images.append(html_img7)


    vals["images"]= "".join(html_images)
    vals["portfolios"]= str(portfolios)
    vals["returns"]= str(returns)
    vals["risks"]= str(risks)
    #print("DONE")
    #print("VALS : ",vals)
    sys.stdout.flush()
    return vals

@app.route("/norm", methods=["GET", "POST"])
def norm():
    global images
    mu,std = float(request.form.get('mu')),float(request.form.get('std'))
    print("MU,STD:",mu,std)
    vals = dict() 
    
    norm = markowitz.normal(mu,std)    
    html_img = img_form.format(norm)
    #images.append(norm)

    vals["normal"]= str(html_img)
    sys.stdout.flush()
    return vals


@app.route("/back", methods=["GET", "POST"])
def back():
    global images
    images = []
    risk_level = int(request.form.get('risk'))
    vals=dict() 
    vals["weights"],images = markowitz.backtest(risk_level=risk_level)
    html_images = [img_form.format(i) for i in images]
    vals["backtest"]= "".join(html_images)

    print("RISK :",risk_level)
    sys.stdout.flush()
    return vals

import report
@app.route("/report", methods=["GET", "POST"])
def make_report():
    name = request.form.get('name')
    print("name: ", name, flush=True)
    report.make_report(name)
    return send_file("/app/pdfs/hello-" + name + ".pdf")


# start flask
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True)
