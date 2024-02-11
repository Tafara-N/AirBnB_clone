#!/usr/bin/python3

"""
Unittests for models/review.py.

Unittest classes:
    TestReviewInstantiation
    TestReviewSave
    TestReviewToDict
"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReviewInstantiation(unittest.TestCase):
    """ Testing the Review class instantiation """

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attr(self):
        review = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(review))
        self.assertNotIn("place_id", review.__dict__)

    def test_user_id_is_public_class_attr(self):
        review = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(review))
        self.assertNotIn("user_id", review.__dict__)

    def test_text_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(review))
        self.assertNotIn("text", review.__dict__)

    def test_two_reviews_unique_ids(self):
        review = Review()
        review1 = Review()
        self.assertNotEqual(review.id, review1.id)

    def test_two_reviews_different_created_at(self):
        review = Review()
        sleep(0.05)
        review1 = Review()
        self.assertLess(review.created_at, review1.created_at)

    def test_two_reviews_different_updated_at(self):
        review = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review.updated_at, review1.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = dt
        rvstr = review.__str__()
        self.assertIn("[Review] (123456)", rvstr)
        self.assertIn("'id': '123456'", rvstr)
        self.assertIn("'created_at': " + dt_repr, rvstr)
        self.assertIn("'updated_at': " + dt_repr, rvstr)

    def test_args_unused(self):
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReviewSave(unittest.TestCase):
    """ Testing the Review class save """

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
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        self.assertLess(first_updated_at, review.updated_at)

    def test_two_saves(self):
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        second_updated_at = review.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        review.save()
        self.assertLess(second_updated_at, review.updated_at)

    def test_save_with_arg(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    def test_save_updates_file(self):
        review = Review()
        review.save()
        rvid = "Review." + rv.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReviewToDict(unittest.TestCase):
    """ Testing the Review class to_dict """

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    def test_to_dict_contains_added_attributes(self):
        review = Review()
        review.middle_name = "Holberton"
        review.my_number = 98
        self.assertEqual("Holberton", review.middle_name)
        self.assertIn("my_number", review.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        review = Review()
        self.assertNotEqual(review.to_dict(), review.__dict__)

    def test_to_dict_with_arg(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict(None)


if __name__ == "__main__":
    unittest.main()
