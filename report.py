import pickle
import pandas as pd
from operations import mprint
from latex import build_pdf
from jinja2 import FileSystemLoader, Template
from latex.jinja2 import make_env


# called in markowitz after graph creations
def latex_pickle_dump(red, blue, new_pie):
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
    risk_new = red['risk']
    risk_curr = blue['risk']

    risk_change = round((risk_new - risk_curr), 2)
    risk_change = stringit(risk_change)
    ret_improve = ret_new - ret_curr

    ret_new = stringit(round(ret_new, 1))
    ret_improve = stringit(round(ret_improve, 1))

    port_vars = {"ret_curr": ret_curr, "risk_curr": risk_curr,
                 "ret_new": ret_new, "risk_new": round(risk_new*100, 2),
                 "risk_change": risk_change, "ret_improve": ret_improve,
                 "new_pie": new_pie}

    with open("port_vars.pickle", 'wb') as port_pickle:
        pickle.dump(port_vars, port_pickle)


def get_preferred_assets(tickers, form_params, asset_map, new_pie):
    tickers = [form_params[t] for t in new_pie]
    asset_classes = [asset_map[t] for t in tickers]

    preferred_dict = {}
    for i in range(len(asset_classes)):
        preferred_dict[asset_classes[i]] = [asset_classes[i], new_pie[asset_map[tickers[i]]]]

    preferred = pd.DataFrame(preferred_dict, index=[preferred_dict[t] for t in asset_classes])
    preferred = preferred.T
    return preferred


def get_captable(captable, form_params, asset_map):
    new_captable = {}
    for t in captable:
        if captable[t] != '0':
            new_captable[asset_map[t]] = captable[t]

    return new_captable


def get_matrices():
    with open("matrices.pickle", 'rb') as pickle_file:
        matrices = pickle.load(pickle_file)
    p, C = matrices

    p = pd.DataFrame(p)
    C = pd.DataFrame(C)

    # mprint("p",p)
    # mprint("C",C)

    return p, C


def get_port_vars(tickers, html_inputs, form_params, asset_map, captable):
    with open("port_vars.pickle", 'rb') as pickle_file:
        port_vars = pickle.load(pickle_file)

    # mprint("html inputs",html_inputs)

    for i in html_inputs:
        port_vars[i] = html_inputs[i]

    for a in form_params:
        if "." in a:
            port_vars[a.replace(".", "")] = form_params[a]
        else:
            port_vars[a.replace(" ", "")] = form_params[a]
        if "^" in form_params[a]:
            port_vars[a.replace(" ", "")] = "\\" + form_params[a][0] + "{}" + form_params[a][1:] #changes


    port_vars["preferred"] = get_preferred_assets(tickers, form_params, asset_map, port_vars['new_pie'])

    captable = get_captable(captable, form_params, asset_map)
    captable = pd.DataFrame(captable, index=[captable[t] for t in captable])
    port_vars['newcap'] = captable.T

    # mprint('cap dframe',port_vars['newcap'])
    # mprint("port vars",port_vars)

    port_vars['p'], port_vars['C'] = get_matrices()

    return port_vars


def make_report(tickers, html_inputs, form_params, asset_map, captable):
    port_vars = get_port_vars(tickers, html_inputs, form_params, asset_map, captable)

    env = make_env(loader=FileSystemLoader('.'))
    tpl = env.get_template('report.tex')

    # create a greeting for all of our friends
    filename = 'pdfs/{} Report.pdf'.format(html_inputs['name'])


    pdf = build_pdf(tpl.render(**port_vars)) #changes
    pdf.save_to(filename)
