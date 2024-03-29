

"""
heehee
app.py
upload contours to s3 with id problem grade IN problems folder
upload full packet images to s3 with id packet grade IN packets folder
"""

# main imports
import os
import json
from flask import Flask, request, render_template, send_file,jsonify,redirect,send_from_directory #reload
from flask_cors import CORS
import sys
import pandas as pd
from datetime import date,datetime

# display whole book
pd.set_option('display.width', 260)
pd.set_option('display.max_columns', 20)

# in-house
import graphs
import report
import markowitz
from operations import mprint


# Initialize the Flask application
app = Flask(__name__, template_folder="templates")
cors = CORS(app)
  
print(app.config,flush=True)
 
# Secret key for passcodes
app.secret_key = b'_5#y2L"g4Q8z\n\xec]/'

images = []
img_form = "{}"
form_params = {}

#stock_symbols                                          # FAQ    https://www.portfoliovisualizer.com/faq#dataSources
form_params["Large Cap Growth"] = "VIGRX"                # FSPGX
form_params["Large Cap Value"] = "JKD"                  # FLCOX S&P 500 Value Index
form_params["Small Cap Growth"] = "^RUT"
form_params["Small Cap Value"] = "VISVX"                # 500 value index not found
form_params["Mid Cap"] = "MDY"                     # identical to ^SP400
form_params["International Stock"] = "VGTSX"            #VTIAX
form_params["Emerging Mkt Stock"] = "VEMAX"
form_params["Intermediate Gov Bonds"] = "GVI"
form_params["Long Gov Bonds"] = "VUSTX"                         #ILTB
form_params["Corporate Bonds"] = "LQD"                          #"CBFSX"         # from JP Morgan   "^SPBDACPT"
form_params["High Yield Bonds"] = "HYG"
form_params["Municipal Bonds"] = "MUB"
form_params["Foreign Bonds"] = "BNDX"                  #BNDX
form_params["Emerging Mkt Debt"] = "JEDAX"
form_params["Real Estate"] = "IYR"              # from Blackrock, models DJSure very very closely   "DJUSRE"
form_params["V.C."] = "VFINX"                       # looks just like LDVIX but goes back to 1980
form_params["Commodities"] = "GSG"            #USCI  # US commodity index instead of dow jones intl. very similar models "^DJCI"
form_params["Cash"] = "BIL"

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')



########################################
########   HOME PAGE ROUTES    #########
########################################

@app.route("/", methods=["GET", "POST"])
@app.route("/finance_home", methods=["GET", "POST"])
def finance_home():
    return render_template("finance_home.html")


@app.route("/crm_home", methods=["GET", "POST"])
def crm_home():
    return render_template("crm_home.html")


@app.route("/team_home", methods=["GET", "POST"])
def team_home():
    return render_template("team_home.html")


########################################
########   FINANCIAL ROUTES    #########
########################################

@app.route("/modules", methods=["GET", "POST"])
def load_home():
    return render_template('index.html')

def get_book(request):
    # get personal info
    info = {'risk': request.form.get('risk'),
            'name': request.form.get('name'),
            'date': str(date.today()),
            'birthday': request.form.get('birthday'),
            'term': request.form.get('term'),
            'firm': 'Greenstar Group',
            'end_date': datetime.strptime(request.form.get('date-input'), '%Y-%m-%d').date(),
            }

    if info['end_date'] is None:
        info['end_date'] = date.today()

    def latex(v):
        return v.replace("^","\\^{}")

    def upper_limit_handle(lim):
        if lim == '':
            return 1
        elif "%" in lim:
            return round(float(lim[:-1])/100,6)
        else:
            return round(float(lim)/100,6)

    def lower_limit_handle(lim):
        if lim == '':
            return 0
        else:
            return upper_limit_handle(lim)

    # get columns for dataframe update
    asset_map = {v: k for k, v in form_params.items()}
    inred = {}
    inblue = {}
    captable = {}
    upperlimit = {}
    lowerlimit = {}

    for v in form_params:
        val = request.form.get(v)
        u_lim = request.form.get(v+"X")
        l_lim = request.form.get(v+"Y")
        ticker = form_params[v]
        # not in blue, not in red
        if val == '' or int(float(val)) == 0:
            captable[ticker] = 0
            upperlimit[ticker] = upper_limit_handle(u_lim)
            lowerlimit[ticker] = lower_limit_handle(l_lim)
            inblue[ticker] = False
        # in blue, in red
        else:
            captable[ticker] = int(float(val))
            upperlimit[ticker] = upper_limit_handle(u_lim)
            lowerlimit[ticker] = lower_limit_handle(l_lim)
            inblue[ticker] = True
        if upper_limit_handle(u_lim) == 0:
            inred[ticker] = False
        else:
            inred[ticker] = True

    #turn 0's to 1's for limit where there is a value in red

    # construct dataframe
    book = pd.DataFrame(captable.items(), columns=['ticker', 'allocation'])
    book['assetclass'] = book['ticker'].map(asset_map)
    book['latex'] = [latex(v) for v in book['ticker']]
    book['inred'] = book['ticker'].map(inred)
    book['inblue'] = book['ticker'].map(inblue)
    book['recommended'] = [0 for i in range(len(form_params))]
    book['upperlimit'] = book['ticker'].map(upperlimit)
    book['lowerlimit'] = book['ticker'].map(lowerlimit)


    # order and sort dataframe
    book = book[['assetclass', 'ticker', 'allocation', 'recommended', 'lowerlimit', 'upperlimit', 'inred', 'inblue', 'latex']]
    book.sort_values('ticker', inplace=True)
    book.reset_index(drop=True, inplace=True)

    mprint('book',book)

    return book, info


@app.route("/load_graphs", methods=["GET", "POST"])
def load_graphs(tickers=None):
    global images

    book, info = get_book(request)

    # mprint("RISK_LEVEL",int(info['risk']))

    images, portfolios, returns, risks = markowitz.markowitz_run(book=book, info=info)
    # images, portfolios, returns, risks = markowitz.markowitz_run(book=book, info=info)

    vals = {'images': str([img_form.format(i) for i in images]),
            'portfolios': str(portfolios),
            'returns': str(returns),
            'risks': str(risks),
            }

    return vals


@app.route("/report", methods=["GET", "POST"])
def make_report():
    book, info = get_book(request)

    report.make_report()

    return send_file("/app/pdfs/{} Report.pdf".format(info['name']))

# start flask
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0")


