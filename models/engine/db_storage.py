from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os

class DBStorage:
    """Database storage engine for SQLAlchemy ORM."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage engine."""
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        HBNB_ENV = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f'mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}',
            pool_pre_ping=True
        )

        # Drop all tables if environment is test
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)
    def rollback(self):
        """Rolls back the current database session"""
        self.__session.rollback()

    def all(self, cls=None):
        """Query all objects or objects of a specific class."""
        if cls:
            objects = self.__session.query(cls).all()
        else:
            objects = []
            for class_type in [State, City, User, Place, Review, Amenity]:
                objects.extend(self.__session.query(class_type).all())

        return {f'{obj.__class__.__name__}.{obj.id}': obj for obj in objects}

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """Close the session."""
        self.__session.close()
