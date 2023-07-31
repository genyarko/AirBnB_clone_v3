#!/usr/bin/python3
""" initialize class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

  @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # Hash the password to MD5 before storing it
        self._password = hashlib.md5(value.encode()).hexdigest()

    def to_dict(self, include_password=False):
        # Call the parent to_dict method and exclude password if needed
        dictionary = super().to_dict()
        if not include_password and 'password' in dictionary:
            del dictionary['password']
        return dictionary

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
