#!/usr/bin/python3
"""
State module for the HBNB project.

Defines the State class and, for FileStorage, a getter for related cities.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

storage_type = os.getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """
    State class
    Attributes for DBStorage:
      - __tablename__ = 'states'
      - name (Column)
      - cities (relationship)
    Attributes/logic for FileStorage:
      - name (string)
      - cities (getter that returns a list of City objects whose state_id = self.id)
    """
    __tablename__ = 'states'

    if storage_type == "db":
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete, delete-orphan"
        )
    else:
        name = ""

        @property
        def cities(self):
            """
            Returns a list of City instances with state_id == current State.id
            Only used if storage_type is 'fs' (FileStorage).
            """
            from models import storage
            from models.city import City
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
