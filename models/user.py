#!/usr/bin/python3

"""
User's class
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    Account user

    Attributes:
        email (str): User's email address
        password (str): User's password
        first_name (str): User's firstname
        last_name (str): User's lastname
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
