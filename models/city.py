#!/usr/bin/python3
"""Module creates a City class"""
from models.base_model import BaseModel


class City(BaseModel):
    """Class manages the city objects"""

    state_id = ""
    name = ""
