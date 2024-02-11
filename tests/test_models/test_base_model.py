#!/usr/bin/python3

"""
Unittests for models/base_model.py.

Unittest classes:
    TestBaseModelInstantiation
    TestBaseModelSave
    TestBaseModelToDict
"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModelInstantiation(unittest.TestCase):
    """ Testing the BaseModel class instantiation """

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        bmodel = BaseModel()
        bmodel1 = BaseModel()
        self.assertNotEqual(bmodel.id, bmodel1.id)

    def test_two_models_different_created_at(self):
        bmodel = BaseModel()
        sleep(0.05)
        bmodel1 = BaseModel()
        self.assertLess(bmodel1.created_at, bmodel1.created_at)

    def test_two_models_different_updated_at(self):
        bmodel = BaseModel()
        sleep(0.05)
        bmodel1 = BaseModel()
        self.assertLess(bmodel.updated_at, bmodel1.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bmodel = BaseModel()
        bmodel.id = "123456"
        bmodel.created_at = bmodel.updated_at = dt
        bmstr = bmodel.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_args_unused(self):
        bmodel = BaseModel(None)
        self.assertNotIn(None, bmodel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bmodel = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bmodel.id, "345")
        self.assertEqual(bmodel.created_at, dt)
        self.assertEqual(bmodel.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bmodel = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bmodel.id, "345")
        self.assertEqual(bmodel.created_at, dt)
        self.assertEqual(bmodel.updated_at, dt)


class TestBaseModelSave(unittest.TestCase):
    """ Testing the BaseModel class save """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
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
        bmodel = BaseModel()
        sleep(0.05)
        first_updated_at = bmodel.updated_at
        bmodel.save()
        self.assertLess(first_updated_at, bmodel.updated_at)

    def test_two_saves(self):
        bmodel = BaseModel()
        sleep(0.05)
        first_updated_at = bmodel.updated_at
        bmodel.save()
        second_updated_at = bmodel.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bmodel.save()
        self.assertLess(second_updated_at, bmodel.updated_at)

    def test_save_with_arg(self):
        bmodel = BaseModel()
        with self.assertRaises(TypeError):
            bmodel.save(None)

    def test_save_updates_file(self):
        bmodel = BaseModel()
        bmodel.save()
        bmid = "BaseModel." + bmodel.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestBaseModelToDict(unittest.TestCase):
    """ Testing the BaseModel class to_dict """

    def test_to_dict_type(self):
        bmodel = BaseModel()
        self.assertTrue(dict, type(bmodel.to_dict()))

    def test_to_dict_has_correct_keys(self):
        bmodel = BaseModel()
        self.assertIn("id", bmodel.to_dict())
        self.assertIn("created_at", bmodel.to_dict())
        self.assertIn("updated_at", bmodel.to_dict())
        self.assertIn("__class__", bmodel.to_dict())

    def test_to_dict_has_added_attr(self):
        bmodel = BaseModel()
        bmodel.name = "Holberton"
        bmodel.my_number = 98
        self.assertIn("name", bmodel.to_dict())
        self.assertIn("my_number", bmodel.to_dict())

    def test_to_dict_datetime_attr_are_strings(self):
        bmodel = BaseModel()
        bm_dict = bmodel.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        bmodel = BaseModel()
        bmodel.id = "123456"
        bmodel.created_at = bmodel.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bmodel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bmodel = BaseModel()
        self.assertNotEqual(bmodel.to_dict(), bmodel.__dict__)

    def test_to_dict_with_arg(self):
        bmodel = BaseModel()
        with self.assertRaises(TypeError):
            bmodel.to_dict(None)


if __name__ == "__main__":
    unittest.main()
