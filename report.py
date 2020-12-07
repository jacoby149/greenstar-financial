import pickle
from latex import build_pdf
from jinja2 import FileSystemLoader
from latex.jinja2 import make_env



def latex_pickle_dump(red, blue):
    def stringit(v):
        if v == 0:
            v = "$\pm$ " + str(v)
        elif v > 0:
            v = "+ " + str(v)
        else:
            v = str(v)
        return v

    ret_new = red['ret']
    ret_curr = blue['ret']
    risk_new = round(red['risk'], 2)
    risk_curr = round(blue['risk'], 2)

    risk_change = round((risk_new - risk_curr), 2)

    risk_change = stringit(risk_change)
    ret_improve = ret_new - ret_curr

    ret_new = stringit(round(ret_new, 1))
    ret_improve = stringit(round(ret_improve, 1))

    port_vars = {"ret_curr": ret_curr, "risk_curr": risk_curr,
                 "ret_new": ret_new, "risk_new": risk_new,
                 "risk_change": risk_change, "ret_improve": ret_improve}

    with open("port_vars.pickle", 'wb') as port_pickle:
        pickle.dump(port_vars, port_pickle)


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
