"""
app.py
upload contours to s3 with id problem grade IN problems folder
upload full packet images to s3 with id packet grade IN packets folder
"""

# imports
import markowitz
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import sys


# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app)

# Do machine Learning Autograding.
@app.route("/", methods=["GET", "POST"])
def load_home():
    return render_template('index.html') #"Hello World!":

@app.route("/mark", methods=["GET", "POST"])
def mark():
    params = request.get_json()
    images,weights,returns,risks = markowitz.rand_data()
    vals = dict() 
    vals["normal"]= str(markowitz.normal())
    vals["images"]= "".join(images)
    vals["weights"]= str(weights)
    vals["returns"]= str(returns)
    vals["risks"]= str(risks)
    #print("DONE")
    #print("VALS : ",vals)
    print("PARAMS :",params)
    sys.stdout.flush()
    return vals

@app.route("/back", methods=["GET", "POST"])
def back():
    params = request.get_json()
    vals = dict() 
    vals["backtest"] = markowitz.backtest()
    print("PARAMS :",params)
    sys.stdout.flush()
    return vals



# start flask
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True)
