#!/usr/bin/python3
"""
Contains module for Basemodel parent class
This class defines every common attributes/methods for other classes
"""

from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """contains a Basemodel parent class
    """

    def __init__(self, *var_args, **var_kwargs):
        """
        Creates instance of BaseModel
        Args:
            *var_args: list of arguments
            **var_kwargs: dict of value arguments
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(var_kwargs) != 0:
            for k, v in var_kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(
                        v, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """
        updates public instance attribute updated_at
        with current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns dictionary containing all values of
        __dict__ of the instance
        1. adds class name to dictionary
        2. Displays time values as strings in isoformat """
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = my_dict['created_at'].isoformat()
        my_dict['updated_at'] = my_dict['updated_at'].isoformat()
        return my_dict

    def __str__(self):
        """
        Print informal string representation of object
        """
        return (f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")
