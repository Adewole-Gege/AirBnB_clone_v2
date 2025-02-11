#!/usr/bin/python3
"""
DBStorage module for the HBNB project.

Contains the DBStorage class that interacts with the MySQL database
using SQLAlchemy ORM.
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
    Manages storage of HBNB models in a MySQL database using SQLAlchemy.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the DBStorage engine using environment variables.
        """
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        HBNB_ENV = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f"mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}"
            f"@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}",
            pool_pre_ping=True
        )

        # Drop all tables if environment is test
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the current database session:
        - If cls is specified, returns all objects of that type.
        - Otherwise, returns all objects of all types.
        """
        if not self.__session:
            self.reload()

        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for c in [State, City, User, Place, Review, Amenity]:
                objs.extend(self.__session.query(c).all())

        return {
            f"{type(obj).__name__}.{obj.id}": obj
            for obj in objs
        }

    def new(self, obj):
        """
        Adds the object to the current database session.
        """
        if self.__session:
            self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session.
        """
        if self.__session:
            self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes obj from the current database session if it’s not None.
        """
        if obj and self.__session:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and initializes a new session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """
        Closes the current SQLAlchemy session using scoped_session.remove().
        """
        if self.__session:
            self.__session.remove()
