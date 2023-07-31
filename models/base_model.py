#!/usr/bin/python3
"""
Contains class BaseModel
"""
import hashlib
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    _password = Column('password', String(128), nullable=False)

    # Property to access password, stored as _password in the database
    @property
    def password(self):
        return self._password

    # Setter to hash the password and store it as _password
    @password.setter
    def password(self, value):
        self._password = hashlib.md5(value.encode()).hexdigest()

    # Method to remove the password key from to_dict()
    # FileStorage uses the parameter include_password=True to include password in to_dict()
    def to_dict(self, include_password=False):
        user_dict = super().to_dict()
        if not include_password:
            user_dict.pop('password', None)
        return user_dict
