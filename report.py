import pickle
from latex import build_pdf
from jinja2 import FileSystemLoader
from latex.jinja2 import make_env

def make_report(name):
    with open("port_vars.pickle", 'rb') as pickle_file:
        port_vars = pickle.load(pickle_file)
    port_vars["name"] = name

    env = make_env(loader=FileSystemLoader('.'))
    tpl = env.get_template('report.tex')

    # create a greeting for all of our friends
    filename = 'pdfs/{} Report.pdf'.format(name)#.lower())

    pdf = build_pdf(tpl.render(**port_vars))
    pdf.save_to(filename)
