#!/usr/bin/python3
"""
Flask application to list states from storage
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Display a HTML page with a list of all State objects sorted by name (A->Z)
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)  # Sort by name
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the SQLAlchemy session after each request"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
