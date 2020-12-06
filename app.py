"""
app.py
upload contours to s3 with id problem grade IN problems folder
upload full packet images to s3 with id packet grade IN packets folder
"""

# imports
import markowitz
from flask import Flask, request, jsonify, render_template, send_file, session, redirect
from flask_cors import CORS
import sys


# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app)

# Secret key for passcodes
app.secret_key = b'_5#y2L"g4Q8z\n\xec]/'

images = []
img_form = "<img src = '{}'>"

form_params = dict()
#stock_symbols
form_params["LargeG"] = "FSPGX"
form_params["LargeV"] = "FLCOX"                # S&P 500 Value Index
form_params["SmallG"] = "^RUT"
form_params["SmallV"] = "FISVX"                # 500 value index not found
form_params["Med"] = "MDY"                     # identical to ^SP400
form_params["Inter"] = "VTIAX"
form_params["Emerging"] = "VEMAX"
form_params["InterBond"] = "GVI"
form_params["Long"] = "ILTB"
form_params["Corp"] = "CBFSX"                  # from JP Morgan   "^SPBDACPT"
form_params["Highyield"] = "HYG"
form_params["Muni"] = "MUB"
form_params["Foreignbonds"] = "BNDX"
form_params["Debt"] = "JEDAX"
form_params["Realestate"] = "IYR"              # from Blackrock, models DJSure very very closely   "DJUSRE"
form_params["V.C."] = "LDVIX"                  # quick replacement from Reuters... need to sus it out   "^AMZX"
form_params["Commodities"] = "USCI"            # US commodity index instead of dow jones intl. very similar models "^DJCI"
form_params["Cash"] = "BIL"


# Do machine Learning.
@app.route("/", methods=["GET", "POST"])
def load_home():
    if 'logged_in'in session:
        return render_template('index.html')
    else:
        return render_template('password_page.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    passcode = request.form.get("passcode")
    if passcode == 'Provins1!':
        session['logged_in'] = True
    return redirect("/")



@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")


def clean_form(request):
    risk = request.form.get('risk')
    name = request.form.get('name')
    birthday = request.form.get('birthday')
    term = request.form.get('term')

    captable = {}
    for v in form_params:
        val = request.form.get(v)
        ticker = form_params[v]
        captable[ticker] = val

    tickers = []
    for k in form_params:
        val = request.form.get(k)
        ticker = form_params[k]
        if val is None:
            continue
        if 'X'.casefold() not in val.casefold() and val != '':
            tickers.append(ticker)

    return captable, tickers, risk, name, birthday, term


@app.route("/load_graphs", methods=["GET", "POST"])
def load_graphs(tickers=None):
    global images
    images = []

    captable, tickers, risk, name, birthday, term = clean_form(request)

    risk=int(risk)
    print("RISK_LEVEL :",risk)
    images,portfolios,returns,risks = markowitz.markowitz_run(tickers=tickers, captable=captable, risk_level=risk)
    # images,portfolios,returns,risks = markowitz.markowitz_run(tickers=None, captable=None, risk_level=risk)
    vals = {}
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

    return vals

@app.route("/norm", methods=["GET", "POST"])
def norm():
    global images
    mu,std = float(request.form.get('mu')),float(request.form.get('std'))
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
    return vals


import report
@app.route("/report", methods=["GET", "POST"])
def make_report():
    _, _, _, name, _, _ = clean_form(request)
    report.make_report(name)

    return send_file("/app/pdfs/{} Report.pdf".format(name))


# start flask
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True)
