#!/usr/bin/python3
"""
Starts a Flask web application that listens on 0.0.0.0, port 5000.

Routes:
    /states_list:
        Displays an HTML page with:
            - An H1 tag with "States"
            - A UL tag with the list of all State objects (from storage)
              sorted by name (A→Z)
              where each LI is formatted as:
                  <state.id>: <B><state.name></B>
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

@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Retrieves all State objects from storage, sorts them by name (A→Z),
    and passes the sorted list to the template.
    """
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
