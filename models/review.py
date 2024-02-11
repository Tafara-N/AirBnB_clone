#!/usr/bin/python3

"""
Reviews class
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Reviews of the place

    Attributes:
        place_id (str): The Place
        user_id (str): The User
        text (str): Reviews
    """

    place_id = ""
    user_id = ""
    text = ""
