import pickle
import pandas as pd
from operations import mprint
from latex import build_pdf
from jinja2 import FileSystemLoader, Template
from latex.jinja2 import make_env



def add_descriptions(book):
    descriptions = {"Large Cap Growth": " Fastly growing stocks from big companies.",
                    "Large Cap Value": " Undervalued stocks from big companies.",
                    "Small Cap Growth": " Fastly growing stocks from small companies.",

                    "Small Cap Value": " Undervalued stocks from small companies.",
                    "Mid Cap": " Stocks from mid sized companies.",
                    "International Stock": " Stocks not traded in U.S.A. exchanges.",

                    "Emerging Mkt Stock": " Stocks from emerging Mkt. countries.",
                    "Real Estate": " Land and buildings.",
                    "V.C.": " New and innovative companies.",

                    "International Gov Bonds": " Govt. bonds that mature in 5-10 years.",
                    "Long Gov Bonds": " Govt. bonds mature in more than 10 years.",

                    "Corporate Bonds": " Bonds issued by a corporation.",
                    "High Yield Bonds": " Lower credit rating higher return bonds.",
                    "Municipal Bonds": " Bonds Issued by local government.",

                    "Foreign Bonds": " Bonds issued in other countries.",
                    "Emerging Mkt Debt": " Bonds issued by emerging countries.",
                    "Commodities": " Basic goods used in commerce.",
                    "Cash": " Currencies, Foreign Currencies."}

    book['description'] = book['assetclass'].map(descriptions)
    return book


# called in markowitz after graph creations
def pickle_dump(red, blue, matrices, book, info):
    def dollar(v):
        if 0 <= v:
            return "\$" + str(v)
        else:
            return "(\$" + str(v)[1:] + ")"

    def percent(v):
        if 0 <= v:
            return str(v) + "\%"
        else:
            return "(" + str(v)[1:] + "\%)"

    book = add_descriptions(book)
    mprint('final final book',book)
    redbook = book[book['infinal']==True]
    bluebook = book[book['inblue']==True]
    ybook = book[(book['inred']==True) | (book['inblue']==True)]

    redret = round(((red['ret'] - 1) * 100),2)
    blueret = round(((blue['ret'] - 1) * 100),2)

    redrisk = round(red['risk']*100,2)
    bluerisk = round(blue['risk']*100,2)

    risk_change = round(redrisk - bluerisk,2)
    ret_change = round(redret - blueret,2)

    p, C = matrices

    report_variables = {"blueret": percent(blueret), "bluerisk": percent(bluerisk),
                        "redret": percent(redret), "redrisk": percent(redrisk),
                        "risk_change": percent(risk_change), "ret_change": percent(ret_change),
                        "book": book, "info": info, "p": p, "C": C,
                        "redbook": redbook, "bluebook": bluebook, "ybook": ybook, }

    with open("report_variables.pickle", 'wb') as report_pickle:
        pickle.dump(report_variables, report_pickle)
# called in markowitz



def make_report():
    # get variables as designed above, passed from markowitz
    with open("report_variables.pickle", 'rb') as pickle_file:
        report_variables = pickle.load(pickle_file)


    env = make_env(loader=FileSystemLoader('.'))
    tpl = env.get_template('report.tex')

    # create a greeting for all of our friends
    filename = 'pdfs/{} Report.pdf'.format(report_variables['info']['name'])


    pdf = build_pdf(tpl.render(**report_variables))
    pdf.save_to(filename)
