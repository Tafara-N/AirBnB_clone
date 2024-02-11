#!/usr/bin/python3

"""
A City class
"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    A city

    Attributes:
        state_id (str): State id.
        name (str): City's name
    """

    state_id = ""
    name = ""
