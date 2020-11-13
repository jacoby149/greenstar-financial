"""
app.py
upload contours to s3 with id problem grade IN problems folder
upload full packet images to s3 with id packet grade IN packets folder
"""

# imports
import markowitz
import multipdf
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import sys


# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app)

images = []
img_form = "<img src = '{}'>"

# Do machine Learning Autograding.
@app.route("/", methods=["GET", "POST"])
def load_home():
    return render_template('index.html') #"Hello World!":

@app.route("/mark", methods=["GET", "POST"])
def mark():
    global images
    images = []
    risk = request.form.get('risk')
    print(risk)
    risk=int(risk)
    print("RISK_LEVEL :",risk)
    images,portfolios,returns,risks = markowitz.markowitz_run(risk_level=risk)
    vals=dict()
    #multipdf.make_pdf(images,"graphs")
    html_images = [img_form.format(i) for i in images]
    vals["images"]= "".join(html_images)
    vals["portfolios"]= str(portfolios)
    vals["returns"]= str(returns)
    vals["risks"]= str(risks)
    #print("DONE")
    #print("VALS : ",vals)
    sys.stdout.flush()
    return vals

@app.route("/norm", methods=["GET", "POST"])
def norm():
    global images
    mu,std = float(request.form.get('mu')),float(request.form.get('std'))
    print("MU,STD:",mu,std)
    vals = dict() 
    norm = markowitz.normal(mu,std)
    html_img = img_form.format(norm)
    images.append(norm)
    multipdf.make_pdf(images,"graphs")
    vals["normal"]= str(html_img)
    sys.stdout.flush()
    return vals


@app.route("/back", methods=["GET", "POST"])
def back():
    global images
    images = []
    risk_level = int(request.form.get('risk'))
    vals=dict() 
    vals["weights"],images = markowitz.backtest(risk_level=risk_level)
    html_images = [img_form.format(i) for i in images]
    multipdf.make_pdf(images,"back")
    vals["backtest"]= "".join(html_images)

    print("RISK :",risk_level)
    sys.stdout.flush()
    return vals



# start flask
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True)
