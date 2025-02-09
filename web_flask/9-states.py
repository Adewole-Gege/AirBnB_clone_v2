#!/usr/bin/python3
"""Flask web application to display states and cities"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the SQLAlchemy session"""
    storage.close()

@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Displays a list of all states or cities of a specific state"""
    states = storage.all(State)
    if id is None:
        return render_template('9-states.html', states=states)
    state = states.get(f'State.{id}')
    return render_template('9-states.html', state=state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
