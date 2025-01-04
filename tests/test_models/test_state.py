#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
import unittest
from models import storage
from models.state import State
import MySQLdb
import os


class TestState(unittest.TestCase, test_basemodel):
    # ... existing test methods ...
    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != 'db', "Not using DBStorage")
    def test_create_state(self):
        """Test creating a new State and checking if it's in the database"""
        # Get initial record count
        db = MySQLdb.connect(user=os.getenv("HBNB_MYSQL_USER"),
                             passwd=os.getenv("HBNB_MYSQL_PWD"),
                             db=os.getenv("HBNB_MYSQL_DB"),
                             host=os.getenv("HBNB_MYSQL_HOST"))
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM states;")
        initial_count = cur.fetchone()[0]

        # Execute console command
        # (Assuming the command is executed using a function called `execute_console_command`)
        execute_console_command("create State name=\"California\"")

        # Get new record count
        cur.execute("SELECT COUNT(*) FROM states;")
        new_count = cur.fetchone()[0]

        # Check if the count increased by 1
        self.assertEqual(new_count, initial_count + 1)

        # Close database connection
        cur.close()
        db.close()


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != 'db', "Not using DBStorage")
def test_update_state_name(self):
    """Test updating a State's name and checking if it's updated in the database"""
    # Create a new State
    new_state = State(name="California")
    new_state.save()

    # Update the State's name
    new_state.name = "New California"
    new_state.save()

    # Retrieve the State from the database
    db = MySQLdb.connect(user=os.getenv("HBNB_MYSQL_USER"),
                         passwd=os.getenv("HBNB_MYSQL_PWD"),
                         db=os.getenv("HBNB_MYSQL_DB"),
                         host=os.getenv("HBNB_MYSQL_HOST"))
    cur = db.cursor()
    cur.execute("SELECT name FROM states WHERE id = %s;", (new_state.id,))
    updated_name = cur.fetchone()[0]

    # Check if the name was updated
    self.assertEqual(updated_name, "New California")

    # Close database connection
    cur.close()
    db.close()


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != 'db', "Not using DBStorage")
def test_delete_state(self):
    """Test deleting a State and checking if it's removed from the database"""
    # Create a new State
    new_state = State(name="California")
    new_state.save()

    # Delete the State
    storage.delete(new_state)
    storage.save()

    # Try to retrieve the State from the database
    db = MySQLdb.connect(user=os.getenv("HBNB_MYSQL_USER"),
                         passwd=os.getenv("HBNB_MYSQL_PWD"),
                         db=os.getenv("HBNB_MYSQL_DB"),
                         host=os.getenv("HBNB_MYSQL_HOST"))
    cur = db.cursor()
    cur.execute("SELECT * FROM states WHERE id = %s;", (new_state.id,))
    result = cur.fetchone()

    # Check if the State was deleted
    self.assertIsNone(result)

    # Close database connection
    cur.close()
    db.close()
