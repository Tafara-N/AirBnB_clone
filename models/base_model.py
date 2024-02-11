#!/usr/bin/python3

"""
The BaseModel class
"""

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    The BaseModel of the AirBnB_clone project."""

    def __init__(self, *args, **kwargs):
        """
        A new BaseModel

        Args:
            *args (any): Unused
            **kwargs (dict): Key: value pairs attributes
        """

        time_form = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, time_form)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """
        Updates updated_at with current datetime
        """

        self.updated_at = datetime.today()
        models.storage.save()

    def to_dictionary(self):
        """
        Dictionary of the BaseModel instance

        Key: value pair __class__ representing the class name of the object
        """
        a_dict = self.__dict__.copy()
        a_dict["created_at"] = self.created_at.isoformat()
        a_dict["updated_at"] = self.updated_at.isoformat()
        a_dict["__class__"] = self.__class__.__name__
        return a_dict

    def __str__(self):
        """
        The print/str representation of the BaseModel instance
        """

        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
