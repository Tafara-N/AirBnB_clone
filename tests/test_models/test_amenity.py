#!/usr/bin/python3

"""
Unittests for models/amenity.py

Unittest classes:
    TestAmenityInstantiation
    TestAmenitySave
    TestAmenityToDictionary
"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenityInstantiation(unittest.TestCase):
    """ Testing the Amenity class instantiation """

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attr(self):
        amty = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amty.__dict__)

    def test_two_amenities_unique_ids(self):
        amty = Amenity()
        amty1 = Amenity()
        self.assertNotEqual(amty.id, amty.id)

    def test_two_amenities_different_created_at(self):
        amty = Amenity()
        sleep(0.05)
        amty1 = Amenity()
        self.assertLess(amty.created_at, amty1.created_at)

    def test_two_amenities_different_updated_at(self):
        amty = Amenity()
        sleep(0.05)
        amty = Amenity()
        self.assertLess(amty.updated_at, amty1.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amty = Amenity()
        amty.id = "123456"
        amty.created_at = amty.updated_at = dt
        amstr = am.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_unused(self):
        amty = Amenity(None)
        self.assertNotIn(None, amty.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """ Instantiation with kwargs """

        dt = datetime.today()
        dt_iso = dt.isoformat()
        amty = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amty.id, "345")
        self.assertEqual(amty.created_at, dt)
        self.assertEqual(amty.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenitySave(unittest.TestCase):
    """ Testing the Amenity class save"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        amty = Amenity()
        sleep(0.05)
        first_updated_at = amty.updated_at
        amty.save()
        self.assertLess(first_updated_at, amty.updated_at)

    def test_two_saves(self):
        amty = Amenity()
        sleep(0.05)
        first_updated_at = amty.updated_at
        amty.save()
        second_updated_at = amty.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amty.save()
        self.assertLess(second_updated_at, amty.updated_at)

    def test_save_with_arg(self):
        amty = Amenity()
        with self.assertRaises(TypeError):
            amty.save(None)

    def test_save_updates_file(self):
        amty = Amenity()
        amty.save()
        amid = "Amenity." + amty.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenityToDict(unittest.TestCase):
    """ Testing the Amenity class to_dict """

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        amty = Amenity()
        self.assertIn("id", amty.to_dict())
        self.assertIn("created_at", amty.to_dict())
        self.assertIn("updated_at", amty.to_dict())
        self.assertIn("__class__", amty.to_dict())

    def test_to_dict_contains_added_attr(self):
        amty = Amenity()
        amty.middle_name = "Holberton"
        amty.my_number = 98
        self.assertEqual("Holberton", amty.middle_name)
        self.assertIn("my_number", amty.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amty = Amenity()
        am_dict = amty.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        amty = Amenity()
        amty.id = "123456"
        amty.created_at = amty.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(amty.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        amty = Amenity()
        self.assertNotEqual(amty.to_dict(), amty.__dict__)

    def test_to_dict_with_arg(self):
        amty = Amenity()
        with self.assertRaises(TypeError):
            amty.to_dict(None)


if __name__ == "__main__":
    unittest.main()
