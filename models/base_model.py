from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid

Base = declarative_base()  # SQLAlchemy declarative base for ORM


class BaseModel:

    """A base class for all hbnb models"""

    # Define SQLAlchemy columns
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())  # Generate a unique ID
            self.created_at = self.updated_at = datetime.utcnow()
        else:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = self.__class__.__name__
        return f"[{cls}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates updated_at and saves the instance to storage"""
        from models import storage  # Lazy import to avoid circular dependency
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Converts the instance into a dictionary"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            # Remove SQLAlchemy state if present
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Deletes the current instance from storage"""
        from models import storage  # Lazy import to avoid circular dependency
        storage.delete(self)
