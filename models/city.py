from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
    """Representation of a city"""
    __tablename__ = 'cities'

    if storage_type == "db":
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)

        places = relationship('Place', backref='cities', cascade='all, delete-orphan')
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """Initialize City instance"""
        super().__init__(*args, **kwargs)

