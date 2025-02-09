#!/usr/bin/python3
"""
Flask application to list states from storage
"""
from flask import Flask, render_template
from models import storage
from models.state import State  # Ensure State model is imported

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display an HTML page with all states"""
    try:
        # ✅ FIX: Use `State` instead of "State"
        states = storage.all(State).values()
        print("DEBUG: Retrieved states:", states)  # Debugging output
        return render_template('7-states_list.html', states=states)
    except Exception as e:
        print("ERROR:", e)  # Print errors
        return "Internal Server Error", 500


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the SQLAlchemy session after each request"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
