#!/usr/bin/python3
"""
Starts a Flask web application that listens on 0.0.0.0:5000.
It defines a single route "/" that returns "Hello HBNB!".
"""

from flask import Flask

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello():
    """Route handler that returns 'Hello HBNB!' when the root URL is accessed."""
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
