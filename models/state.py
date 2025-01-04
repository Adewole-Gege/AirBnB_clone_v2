from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if storage_type == "db":
        # Define SQLAlchemy columns
        name = Column(String(128), nullable=False)

        # Define relationship with City
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ""

    @property
    def cities(self):
        """Getter attribute for FileStorage relationship.
        Returns the list of City instances with state_id
        matching the current State id.
        """
        from models import storage
        from models.city import City
        city_list = []
        for city in storage.all(City).values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
