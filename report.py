import pickle
import pandas as pd
from operations import mprint
from latex import build_pdf
from jinja2 import FileSystemLoader, Template
from latex.jinja2 import make_env



def dollar(v):
    if 0 <= v:
        return "\$" + '{:,}'.format(int(v))
    else:
        return "(\$" + '{:,}'.format(int(v))[1:] + ")"


def percent(v):
    if 0 <= v:
        return str(v) + "\%"
    else:
        return "(" + str(v)[1:] + "\%)"



def latexify(book, info):
    book['change'] = book['change'].apply(dollar)
    book['allocation'] = book['allocation'].apply(dollar)
    book['recommended'] = book['recommended'].apply(dollar)

    info['wealth'] = dollar(info['wealth'])
    info['redoneret'] = dollar(info['redoneret'])
    info['redsevenret'] = dollar(info['redsevenret'])
    info['blueoneret'] = dollar(info['blueoneret'])
    info['bluesevenret'] = dollar(info['bluesevenret'])
    info['redoneretchange'] = percent(round(info['redoneretchange']*100,2))
    info['redsevenretchange'] = percent(round(info['redsevenretchange']*100,2))
    info['blueoneretchange'] = percent(round(info['blueoneretchange']*100,2))
    info['bluesevenretchange'] = percent(round(info['bluesevenretchange']*100,2))


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

    return book, info


def write_montecarlo(info):
    red_one_year = info['rlinedata'][1]
    info['redoneret'] = red_one_year[0]
    info['redonerisk'] = percent(round(red_one_year[1]/100,2))

    red_seven_year = info['rlinedata'][7]
    info['redsevenret'] = red_seven_year[0]
    info['redsevenrisk'] = percent(round(red_seven_year[1]/100,2))

    blue_one_year = info['blinedata'][1]
    info['blueoneret'] = blue_one_year[0]
    info['blueonerisk'] = percent(round(blue_one_year[1]/100,2))

    blue_seven_year = info['blinedata'][7]
    info['bluesevenret'] = blue_seven_year[0]
    info['bluesevenrisk'] = percent(round(blue_seven_year[1]/100,2))

    info['redoneretchange'] = (info['redoneret'] - info['wealth']) / info['wealth']
    info['redsevenretchange'] = (info['redsevenret'] - info['wealth']) / info['wealth']
    info['blueoneretchange'] = (info['blueoneret'] - info['wealth']) / info['wealth']
    info['bluesevenretchange'] = (info['bluesevenret'] - info['wealth']) / info['wealth']

    return info


# called in markowitz after graph creations
def pickle_dump(red, blue, matrices, book, info):
    p, C = matrices

    redret = round(((red['ret']-1)*100),2)
    blueret = round(((blue['ret']-1)*100),2)

    redrisk = round(red['risk']*100,2)
    bluerisk = round(blue['risk']*100,2)

    risk_change = round(redrisk - bluerisk,2)
    ret_change = round(redret - blueret,2)

    info = write_montecarlo(info)


    # convert book, info to LaTex friendly formatting
    book, info = latexify(book, info)

    mprint('latex book',book)
    redbook = book[book['infinal']==True]
    bluebook = book[book['inblue']==True]
    ybook = book[(book['inred']==True) | (book['inblue']==True)]


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
