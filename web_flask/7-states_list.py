#!/usr/bin/python3
"""
Starts a Flask web application that listens on 0.0.0.0, port 5000.
Routes:
    /states_list: Displays an HTML page with a list of all State objects.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the current SQLAlchemy session after each request.
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Displays an HTML page listing all State objects present in DBStorage,
    sorted by name (A->Z).
    """
    # Sort the states by name A->Z
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
