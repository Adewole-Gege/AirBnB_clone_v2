#!/usr/bin/python3
"""Flask application with dynamic routes."""
from flask import Flask

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Returns Hello HBNB!"""
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns HBNB"""
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """Returns C followed by the text"""
    return "C {}".format(text.replace("_", " "))

@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    """Returns Python followed by the text"""
    return "Python {}".format(text.replace("_", " "))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

