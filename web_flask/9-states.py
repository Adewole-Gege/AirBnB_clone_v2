#!/usr/bin/python3
"""
Flask web application to display States and their Cities.

Routes:
    /states:
        Displays an HTML page with all State objects (from storage)
        sorted by name (A→Z). Each state is rendered as:
            <state.id>: <B><state.name></B>
    /states/<state_id>:
        If a State with the given id is found, displays:
            <H1>State: <state.name></H1>
            <H3>Cities:</H3>
            <UL> with each City (sorted by name A→Z) as:
                <city.id>: <B><city.name></B>
        Otherwise, displays:
            <H1>Not found!</H1>

After each request, the current SQLAlchemy session is closed.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the current SQLAlchemy session after each request."""
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    """
    Retrieves all State objects from storage, sorts them by name (A→Z),
    and passes them to the template along with state=None.
    """
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template('9-states.html', states=states, state=None)


@app.route('/states/<state_id>', strict_slashes=False)
def state_detail(state_id):
    """
    Retrieves the State with the given id from storage.
    If found, sorts its cities by name (A→Z) and passes both to the template.
    If not found, passes state=None so that the template displays "Not found!".
    """
    state = storage.all(State).get("State." + state_id)
    if state is None:
        return render_template('9-states.html', state=None)
    cities = sorted(state.cities, key=lambda c: c.name)
    return render_template('9-states.html', state=state, cities=cities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
