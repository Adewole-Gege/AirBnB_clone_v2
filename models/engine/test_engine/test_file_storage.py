#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py"""
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User


class TestFileStorage(unittest.TestCase):
    """Unittests for testing the FileStorage class."""

    def setUp(self):
        """Set up test methods."""
        self.storage = FileStorage()
        self.obj = BaseModel()
        self.user = User(email="test@example.com", password="test")
        self.storage.new(self.obj)
        self.storage.new(self.user)

    def tearDown(self):
        """Tear down test methods."""
        del self.storage
        del self.obj
        del self.user

    def test_all(self):
        """Test the all method."""
        all_objects = self.storage.all()
        self.assertIn(f"BaseModel.{self.obj.id}", all_objects)
        self.assertIn(f"User.{self.user.id}", all_objects)

    def test_all_with_class(self):
        """Test the all method with a class filter."""
        all_users = self.storage.all(User)
        self.assertIn(f"User.{self.user.id}", all_users)
        self.assertNotIn(f"BaseModel.{self.obj.id}", all_users)

    def test_delete(self):
        """Test the delete method."""
        key = f"BaseModel.{self.obj.id}"
        self.assertIn(key, self.storage.all())
        self.storage.delete(self.obj)
        self.assertNotIn(key, self.storage.all())
        self.storage.delete(None) 


if __name__ == "__main__":
    unittest.main()
