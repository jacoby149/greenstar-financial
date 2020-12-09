"""
app.py
upload contours to s3 with id problem grade IN problems folder
upload full packet images to s3 with id packet grade IN packets folder
"""

# main imports
from flask import Flask, request, jsonify, render_template, send_file, session, redirect
from flask_cors import CORS
import sys
import pandas as pd

# in-house
import graphs
import report
import markowitz
from operations import mprint


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



# do machine learning
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


def get_book(request):
    # get personal info
    info = {'risk': request.form.get('risk'),
            'name': request.form.get('name'),
            'birthday': request.form.get('birthday'),
            'term': request.form.get('term'),
            'firm': 'Provins',
            }

    # get columns for dataframe
    asset_map = {v: k for k, v in form_params.items()}
    inred = {}
    inblue = {}

    captable = {}
    for v in form_params:
        val = request.form.get(v)
        ticker = form_params[v]
        if val == '':
            captable[ticker] = 0
            inred[ticker] = False
            inblue[ticker] = False
        elif 'X'.casefold() in val.casefold():
            captable[ticker] = int(val[:len(val)-1])
            inred[ticker] = False
            inblue[ticker] = True
        elif val == '0':
            captable[ticker] = 0
            inred[ticker] = True
            inblue[ticker] = False
        else:
            captable[ticker] = int(val)
            inred[ticker] = True
            inblue[ticker] = True

    # construct dataframe
    book = pd.DataFrame(captable.items(), columns=['ticker', 'allocation'])
    book['assetclass'] = book['ticker'].map(asset_map)
    book['inred'] = book['ticker'].map(inred)
    book['inblue'] = book['ticker'].map(inblue)
    book['recommended'] = [0 for i in range(len(form_params))]


    # order and sort dataframe
    book = book[['assetclass', 'ticker', 'allocation', 'recommended', 'inred', 'inblue']]
    book.sort_values('ticker', inplace=True)
    book.set_index('ticker', inplace=True)

    mprint('book',book)

    return book, info


@app.route("/load_graphs", methods=["GET", "POST"])
def load_graphs(tickers=None):
    global images

    book, info = get_book(request)

    # mprint("RISK_LEVEL",int(info['risk']))

    images, portfolios, returns, risks = markowitz.markowitz_run(book=book, info=info)
    # images, portfolios, returns, risks = markowitz.markowitz_run(book=book, info=info)

    vals = {'images': "".join([img_form.format(i) for i in images]),
            'portfolios': str(portfolios),
            'returns': str(returns),
            'risks': str(risks),
            }

    return vals


@app.route("/report", methods=["GET", "POST"])
def make_report():
    book, info = get_book(request)

    report.make_report(book=book, info=info)

    return send_file("/app/pdfs/{} Report.pdf".format(info['name']))


# @app.route("/back", methods=["GET", "POST"])
# def back():
#     global images
#     images = []
#     risk_level = int(request.form.get('risk'))
#     vals=dict()
#     vals["weights"],images = markowitz.backtest(risk_level=risk_level)
#     html_images = [img_form.format(i) for i in images]
#     vals["backtest"]= "".join(html_images)
#     return vals


# start flask
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True)


