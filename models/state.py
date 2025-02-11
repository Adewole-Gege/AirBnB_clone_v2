#!/usr/bin/python3
"""
State module for the HBNB project.

Contains the State class and a FileStorage-only getter for related City objects.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

storage_type = os.getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """
    State class that represents a US state.

    In DBStorage mode:
      - name is a column in the 'states' table.
      - 'cities' is a relationship to City.
    In FileStorage mode:
      - name is just an attribute.
      - 'cities' is a getter property that returns a list of City instances.
    """
    __tablename__ = 'states'

    if storage_type == "db":
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City',
            backref='state',
            cascade='all, delete, delete-orphan'
        )
    else:
        name = ""

        @property
        def cities(self):
            """
            Returns the list of City instances where City.state_id == current State.id.
            This is only used when FileStorage is being used.
            """
            from models import storage
            from models.city import City
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
