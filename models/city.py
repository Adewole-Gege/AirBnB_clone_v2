from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
<<<<<<< HEAD
from models.place import Place
from os import getenv


=======
from os import getenv

>>>>>>> main
storage_type = getenv("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
<<<<<<< HEAD
=======
    """Representation of a city"""
>>>>>>> main
    __tablename__ = 'cities'

    if storage_type == "db":
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)

<<<<<<< HEAD
        places = relationship('Place', backref='cities',
                              cascade='all, delete-orphan')
    else:
        name = ""
        state_id = ""
=======
        places = relationship('Place', backref='cities', cascade='all, delete-orphan')
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """Initialize City instance"""
        super().__init__(*args, **kwargs)

>>>>>>> main
