"""
app.py
upload contours to s3 with id problem grade IN problems folder
upload full packet images to s3 with id packet grade IN packets folder
"""

# imports
import markowitz
from operations import *
import graphs
from flask import Flask, request, jsonify, render_template, send_file, session, redirect
from flask_cors import CORS
import sys
import pandas as pd


# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app)

# Secret key for passcodes
app.secret_key = b'_5#y2L"g4Q8z\n\xec]/'

images = []
img_form = "<img src = '{}'>"

form_params = dict()
#stock_symbols
form_params["Large Cap Growth"] = "VIGRX"                # FSPGX
form_params["Large Cap Val"] = "JKD"                  # FLCOX S&P 500 Value Index
form_params["Small Cap Growth"] = "^RUT"
form_params["Small Cap Val"] = "VISVX"                # 500 value index not found
form_params["Mid Cap"] = "MDY"                     # identical to ^SP400
form_params["Intl Stock"] = "VTIAX"
form_params["Emerging Mkt Stock"] = "VEMAX"
form_params["Intl Gov Bonds"] = "GVI"
form_params["Long Gov Bonds"] = "ILTB"
form_params["Corporate Bonds"] = "CBFSX"                  # from JP Morgan   "^SPBDACPT"
form_params["High Yield Bonds"] = "HYG"
form_params["Municipal Bonds"] = "MUB"
form_params["Foreign Bonds"] = "BNDX"
form_params["Emerging Mkt Debt"] = "JEDAX"
form_params["Real Estate"] = "IYR"              # from Blackrock, models DJSure very very closely   "DJUSRE"
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
    asset_map = {v: k for k, v in form_params.items()}

    risk = request.form.get('risk')
    name = request.form.get('name')
    birthday = request.form.get('birthday')
    term = request.form.get('term')

    personal_info = {'risk': risk, 'name': name, 'birthday': birthday, 'term': term, 'firm': 'Provins'}
    recommended = ['-' for i in range(len(form_params))]


    captable = {}
    for v in form_params:
        val = request.form.get(v)
        ticker = form_params[v]
        if val == '':
            captable[ticker] = '-'
        else:
            captable[ticker] = val

    book = pd.DataFrame(captable.items(), columns=['ticker', 'allocation'])
    book['assetclass'] = book['ticker'].map(asset_map)
    book['recommended'] = recommended

    book = book[['assetclass', 'ticker', 'allocation', 'recommended']]
    log('book',book)

    return book, personal_info


@app.route("/load_graphs", methods=["GET", "POST"])
def load_graphs(tickers=None):
    global images
    global asset_map
    images = []

    captable, tickers, risk, name, birthday, term, old_tickers = clean_form(request)

    risk=int(risk)
    print("RISK_LEVEL :",risk)
    images,portfolios,returns,risks = markowitz.markowitz_run(tickers=tickers, captable=captable, risk_level=risk, old_tickers=old_tickers, asset_map=asset_map)
    # images,portfolios,returns,risks = markowitz.markowitz_run(tickers=None, captable=None, risk_level=risk, old_tickers=None, asset_map=form_params)
    vals = {}
    html_images = [img_form.format(i) for i in images]


    vals["images"]= "".join(html_images)
    vals["portfolios"]= str(portfolios)
    vals["returns"]= str(returns)
    vals["risks"]= str(risks)

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
    global form_params
    global asset_map


    captable, tickers, risk, name, birthday, term, _ = clean_form(request)
    html_inputs = {'risk': risk, 'name': name, 'birthday': birthday, 'term': term}

    report.make_report(tickers, html_inputs, form_params, asset_map, captable)

    return send_file("/app/pdfs/{} Report.pdf".format(name))


# start flask
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True)
