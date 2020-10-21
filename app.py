"""
app.py
upload contours to s3 with id problem grade IN problems folder
upload full packet images to s3 with id packet grade IN packets folder
"""


# imports
import markowitz
from flask import Flask, request, jsonify
from flask_cors import CORS


# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app)

# Do machine Learning Autograding.
@app.route("/", methods=["GET", "POST"])
def markowitz_print():
    images,weights,returns,risks = markowitz.rand_data()
    return "".join(images)+ "\n" + str(weights)#+str(returns)+str(risks)

# start flask
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True)
