#!/usr/bin/python3
"""
DBStorage module for the HBNB project.

This module defines a class to manage storage of HBNB models in a MySQL database using SQLAlchemy.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """
    Interacts with the MySQL database using SQLAlchemy ORM.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the DBStorage engine using environment variables.
        """
        HBNB_MYSQL_USER = os.getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = os.getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = os.getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = os.getenv("HBNB_MYSQL_DB")
        HBNB_ENV = os.getenv("HBNB_ENV")

        self.__engine = create_engine(
            f"mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}"
            f"@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}",
            pool_pre_ping=True
        )

        # Drop all tables if the environment is test
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the current database session for all objects of type cls.
        If cls is None, queries all objects of all types.
        Returns a dictionary: {<class name>.<id>: obj}
        """
        obj_dict = {}
        classes = [State, City, User, Place, Review, Amenity]
        if cls:
            if not isinstance(cls, list):
                classes = [cls]
        for c in classes:
            for obj in self.__session.query(c).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """
        Adds obj to the current database session.
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes obj from the current database session if not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and initializes a new session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """
        Calls remove() on the current SQLAlchemy session to ensure that a new
        session is created upon next use.
        """
        if self.__session:
            self.__session.remove()
