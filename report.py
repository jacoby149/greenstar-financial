
from latex import build_pdf
from jinja2 import FileSystemLoader
from latex.jinja2 import make_env

def make_report(name):

    # create a jinja2 environment with latex-compatible markup and instantiate a
    # template
    env = make_env(loader=FileSystemLoader('.'))
    tpl = env.get_template('report.tex')

    if name == '':
        return "Please enter your name"

    # create a greeting for all of our friends
    filename = 'pdfs/hello-{}.pdf'.format(name.lower())


    pdf = build_pdf(tpl.render(name=name))
    pdf.save_to(filename)
