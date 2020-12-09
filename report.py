import pickle
import pandas as pd
from operations import mprint
from latex import build_pdf
from jinja2 import FileSystemLoader, Template
from latex.jinja2 import make_env


# called in markowitz after graph creations
def pickle_dump(red, blue, matrices, book, info):
    def stringit(v):
        if v == 0:
            v = "$\pm$ " + str(v)
        elif v > 0:
            v = "+ " + str(v)
        else:
            v = str(v)
        return v

    redret = red['ret']
    blueret = blue['ret']
    redrisk = red['risk']
    bluerisk = blue['risk']

    risk_change = round((risk_new - risk_curr), 2)
    risk_change = stringit(risk_change)
    ret_change = ret_new - ret_curr

    ret_new = stringit(round(ret_new, 1))
    ret_change = stringit(round(ret_change, 1))

    p, C = matrices

    report_variables = {"blueret": blueret, "bluerisk": bluerisk,
                        "redret": redret, "redrisk": round(redrisk*100, 2),
                        "risk_change": risk_change, "ret_change": ret_change,
                        "book": book, "info": info, "p": p, "C": C, }

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
    filename = 'pdfs/{} Report.pdf'.format(html_inputs['name'])


    pdf = build_pdf(tpl.render(**report_variables))
    pdf.save_to(filename)
