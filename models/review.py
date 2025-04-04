#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE")


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = 'reviews'
    if storage_type == 'db':

        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        # place = relationship('Place', backref='reviews')
        # user = relationship('User', backref='reviews')
    else:
        place_id = ""
        user_id = ""
        text = ""
<<<<<<< HEAD
=======

>>>>>>> main
