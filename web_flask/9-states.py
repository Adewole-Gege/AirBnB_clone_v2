#!/usr/bin/python3
"""
Flask web application to display States and their Cities.
Routes:
    /states:
        - Displays an HTML page with all State objects (sorted by name).
        - Each state is rendered as: <state.id>: <B><state.name></B>
    /states/<state_id>:
        - If a State with the given id exists:
            * H1 tag: "State: <state.name>"
            * H3 tag: "Cities:"
            * UL listing each City (sorted by name) as: <city.id>: <B><city.name></B>
        - Otherwise:
            * H1 tag: "Not found!"
After each request, the current SQLAlchemy session is closed.
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


@app.route('/states', strict_slashes=False)
def states_list():
    """
    Displays all State objects sorted by name.
    """
    states_dict = storage.all(State)
    # Convert to a list and sort by state.name in ascending order
    states = sorted(states_dict.values(), key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<state_id>', strict_slashes=False)
def state_detail(state_id):
    """
    Displays the details for a specific State and its Cities.
    If found, sorts the State's cities by name.
    Otherwise, returns a page with "Not found!".
    """
    states_dict = storage.all(State)
    state = states_dict.get(f"State.{state_id}")
    if state:
        # Sort the cities of the found state by name
        cities = sorted(state.cities, key=lambda city: city.name)
    else:
        cities = None
    return render_template('9-states.html', state=state, cities=cities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
