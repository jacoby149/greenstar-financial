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

                    "Intermediate Gov Bonds": " Govt. bonds that mature in 5-10 years.",
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
    info['redoneret'] = red_one_year[0] - info['wealth']
    info['redonerisk'] = percent(round(red_one_year[1]/100,2))

    red_seven_year = info['rlinedata'][7]
    info['redsevenret'] = red_seven_year[0] - info['wealth']
    info['redsevenrisk'] = percent(round(red_seven_year[1]/100,2))

    blue_one_year = info['blinedata'][1]
    info['blueoneret'] = blue_one_year[0] - info['wealth']
    info['blueonerisk'] = percent(round(blue_one_year[1]/100,2))

    blue_seven_year = info['blinedata'][7]
    info['bluesevenret'] = blue_seven_year[0] - info['wealth']
    info['bluesevenrisk'] = percent(round(blue_seven_year[1]/100,2))

    info['redoneretchange'] = info['redoneret'] / info['wealth']
    info['redsevenretchange'] = info['redsevenret'] / info['wealth']
    info['blueoneretchange'] = info['blueoneret'] / info['wealth']
    info['bluesevenretchange'] = info['bluesevenret'] / info['wealth']

    return info




# Corr. & MSFT & NTFX & HULU  & RUS & BP & TR & SOCK \\\midrule
# MSFT  & 16.128 & +8.872 & 16.128 & 1.402 & 1.373 & -146.6 & -137.6 \\\midrule
# NTFX  & 3.442  & -2.509 & 3.442  & 0.299 & 0.343 & 133.2  & 152.4  \\\midrule
# HULU  & 1.826  & -0.363 & 1.826  & 0.159 & 0.119 & 168.5  & -161.1 \\\midrule
# RUS  & 0.993  & -0.429 & 0.993  & 0.086 & 0.08  & 25.6   & 90     \\ \midrule
# BP  & 1.29   & +0.099 & 1.29   & 0.112 & 0.097 & -175.6 & -114.7 \\\midrule
# TR  & 0.483  & -0.183 & 0.483  & 0.042 & 0.063 & 22.3   & 122.5  \\\midrule
# SOCK  & 0.766  & -0.475 & 0.766  & 0.067 & 0.039 & 141.6  & -122    \\\bottomrule

def latex_matrix(C):
    def semantic(j):
        if 0 < j:
            if j == 1:
                color = "{0,0,0}"
            else:
                color = "{0,"+str(abs(j/2))+","+str(abs(j/4))+"}"
        elif j < 0:
            color = "{"+str(abs(j))+",0,0}"
        return "\\color[rgb]"+color+" "+str(j)+" \\color{black}"


    tickers = C.columns.tolist()
    tags = ''.join(['c' for c in range(C.shape[0] + 1)])
    header = ' \\begin{tabular}{' + tags + '}\n \\toprule \n'
    footer = ' \\\\ \n \\bottomrule \n \\end{tabular} \n'

    row1 = 'Corr. '
    for i in range(C.shape[0]):
        row1 = row1 +' & ' + tickers[i]

    body = ''
    for i in C:
        body = body + ' \\\\ \n \\midrule \n' + i
        for j in C[i]:
            body = body + ' & ' + semantic(j)


    table = header + row1 + body + footer
    return table



# called in markowitz after graph creations
def pickle_dump(red, blue, C, book, info):
    def profit_cent(v):
        v = int((100*v)-100)
        if 0 <= v:
            return str(v) + "%"
        else:
            return "(" + str(v)[1:] + "%)"

    def risk_cent(v):
        v = int((100*v))
        if 0 <= v:
            return str(v) + "%"
        else:
            return "(" + str(v)[1:] + "%)"

    p = info['p']
    p = p.apply(lambda x: x.apply(profit_cent))
    p = p.to_latex(index=False)

    r = info['r']
    r = r.apply(lambda x: x.apply(risk_cent))
    r = r.to_latex(index=False)

    redret = round((red['ret']*100),2)
    blueret = round((blue['ret']*100),2)

    redrisk = round(red['risk']*100,2)
    bluerisk = round(blue['risk']*100,2)

    riskchange = round(redrisk - bluerisk,2)
    retchange = round(redret - blueret,2)

    info = write_montecarlo(info)

    C = latex_matrix(C)

    # convert book, info to LaTex friendly formatting
    book, info = latexify(book, info)

    # mprint('latex book',book)
    redbook = book[book['infinal']==True ]
    bluebook = book[book['inblue']==True]
    ybook = book[(book['inred']==True) | (book['inblue']==True)]


    report_variables = {"blueret": percent(blueret), "bluerisk": percent(bluerisk),
                        "redret": percent(redret), "redrisk": percent(redrisk),
                        "riskchange": percent(riskchange), "retchange": percent(retchange),
                        "book": book, "info": info, "p": p, "C": C, "r": r,
                        "redbook": redbook, "bluebook": bluebook, "ybook": ybook, }

    with open("report_variables.pickle", 'wb') as report_pickle:
        pickle.dump(report_variables, report_pickle)
# called in markowitz



def make_report(client='demo'):
    # get variables as designed above, passed from markowitz
    with open("report_variables.pickle", 'rb') as pickle_file:
        report_variables = pickle.load(pickle_file)

    template = 'Clients/{}/report.tex'.format(client)

    env = make_env(loader=FileSystemLoader('.'))
    tpl = env.get_template(template)

    # create a greeting for all of our friends
    filename = 'pdfs/{} Report.pdf'.format(report_variables['info']['name'])


    pdf = build_pdf(tpl.render(**report_variables))
    pdf.save_to(filename)
