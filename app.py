"""
app.py
upload contours to s3 with id problem grade IN problems folder
upload full packet images to s3 with id packet grade IN packets folder
"""

# main imports
import os
import json
from flask import Flask, request, render_template, send_file, session, redirect,send_from_directory #reload
from flask_cors import CORS
import sys
import pandas as pd
from datetime import date,datetime
from query import *

# display whole book
pd.set_option('display.width', 260)
pd.set_option('display.max_columns', 20)

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
form_params["Foreign Bonds"] = "PIGLX"                  #BNDX
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
    if 'logged_in' in session and session['logged_in'] == True:
        return render_template('index.html', **session)
    else:
        return render_template('password_page.html')
    

@app.route("/login", methods=["GET", "POST"])
def login():
    passcode = request.form.get("passcode")
    eq_dict = {'passcode' : passcode}
    resp = select_query("clients",eq_dict)

    print(passcode,"\n",resp,flush=True)
    if (len(resp)>0):
        client = resp[0]
        session['logged_in'] = True
        session['client'] = client["name"]
        session['rolodex'] = client["rolodex"]
        session['directory'] = client['directory_name']
        session['image'] = "static/img/{}".format(client["logo"])
        session['title'] = "{} Custom Algorithms - {}".format(client["firm"],client["header_title"])       
    return redirect("/modules")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/modules")


def get_book(request):
    # get personal info
    info = {'risk': request.form.get('risk'),
            'name': request.form.get('name'),
            'date': str(date.today()),
            'birthday': request.form.get('birthday'),
            'term': request.form.get('term'),
            'firm': 'Provins',
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

    report.make_report(session['directory'])

    return send_file("/app/pdfs/{} Report.pdf".format(info['name']))


# ########################################
# ########      CRM ROUTES       #########
# ########################################
 
#Logging out of CRM
@app.route("/crm_logout", methods=["GET", "POST"])
def crm_logout():
    session.clear()
    return redirect("/crm")

#Verify a submitted CRM login attempt
@app.route("/crm_verify", methods=["GET", "POST"])
def crm_verify():
    passcode = request.form.get("passcode")
    eq_dict = {'passcode' : passcode}
    resp = select_query("clients",eq_dict)

    print(passcode,"\n",resp,flush=True)
    if (len(resp)>0):
        client = resp[0]
        session['logged_in'] = True
        session['directory'] = client['directory_name']
        session['rolodex'] = client["rolodex"]
        session['client'] = client["name"]
        session['image'] = "static/img/{}".format(client["logo"])
    return redirect("/crm")

#CRM Dashboard
@app.route("/crm", methods=["GET", "POST"])
def crm():
    if 'logged_in' in session and session['logged_in'] == True:
        return render_template('crm.html', **session)
    else:
        return render_template('crm_password_page.html')

#Loading of contacts into the CRM dashboard
@app.route("/load_contacts", methods=["GET", "POST"])
def load_contacts():
    eq_dict = {'rolodex':session['rolodex']}#,'archived':("IS",None)}
    contacts = select_query("contacts",eq_dict)
    return json.dumps(contacts)

#Loading all notes for a contact
@app.route("/load_notes", methods=["GET", "POST"])
def load_notes():
    eq_dict = {"contact_id" : request.form.get('id')}
    notes = select_query("notes",eq_dict,'date')
    #TODO jsonify notes
    return notes

#Loading all ledger entries for a contact
@app.route("/load_ledger", methods=["GET", "POST"])
def load_ledge():
    eq_dict = {"contact_id" : request.form.get('id')}
    ledger = select_query("ledger",eq_dict,'date')
    #TODO jsonify notes
    return ledger


#Adding a contact to the DB and ...
@app.route("/add_contact", methods=["GET", "POST"])
def add_contact():
    name = request.form.get("name")
    company = request.form.get("company")
    phone = request.form.get("phone")
    email = request.form.get("email")
    rolodex = request.form.get("rolodex")
    insert_dict = {'name':name,'company':company,
            'phone':phone,'email':email,
                'rolodex':rolodex}
    #TODO get id from mysql python insert query
    return insert_query('contacts',insert_dict)

#Submitting a ledge for a contact
@app.route("/add_note", methods=["GET", "POST"])
def add_notes():
    contact_id = request.form.get("id")
    note = request.form.get("note")    
    date = str(datetime.now())
    insert_dict = {'contact_id':contact_id,'note':note,'date':date}
    note_id = insert_query('notes',insert_dict)
    return note_id

#Submitting a ledge for a contact
@app.route("/add_ledge", methods=["GET", "POST"])
def add_ledge():

    contact_id = request.form.get('contact_id')
    amount = request.form.get('amount')
    check_number = request.form.get('check_number')
    description = request.form.get('description')
    date = request.form.get('date')
    recurring = request.form.get('recurring')
    
    insert_dict = {'contact_id':contact_id,'amount':amount,
            'check_number':check_number,'description':description,
                'date':date,'recurring':recurring} 
    
    ledge_id = insert_query('ledger',insert_dict)
    return ledge_id

#Removing a contact from the DB and ...
@app.route("/remove_contact", methods=["GET", "POST"])
def remove_contact():
    name = request.form.get('name')
    company = request.form.get('company')
    phone = request.form.get('phone')
    email = request.form.get('email')
    eq_dict = {'name':name,'company':company,'phone':phone,'email':email}
    insert_dict = {'archived': str(datetime.now()) }
    update_query('contacts',eq_dict,insert_dict)    
    return "success"

# start flask
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True)


