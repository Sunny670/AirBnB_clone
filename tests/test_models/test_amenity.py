#!/usr/bin/python3
"""Unittests for models/amenity.py.

Unittest classes included:
    TestAmenity_instantiation
    TestAmenity_to_dict
    TestAmenity_save
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittest for testing instantiation of Amenity class."""

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))
        
    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))
        
    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        amm = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amm.__dict__)

    def test_two_amenities_unique_ids(self):
        amm1 = Amenity()
        amm2 = Amenity()
        self.assertNotEqual(amm1.id, amm2.id)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amm = Amenity()
        amm.id = "123456"
        amm.created_at = amm.updated_at = dt
        amstr = amm.__str__()
        self.assertIn("[Amenity] (123456)", ammstr)
        self.assertIn("'id': '123456'", ammstr)
        self.assertIn("'created_at': " + dt_repr, ammstr)
        self.assertIn("'updated_at': " + dt_repr, ammstr)

    def test_args_unused(self):
        amm = Amenity(None)
        self.assertNotIn(None, amm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amm = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amm.id, "345")
        self.assertEqual(amm.created_at, dt)
        self.assertEqual(amm.updated_at, dt)

    def test_two_amenities_different_updated_at(self):
        amm1 = Amenity()
        sleep(0.05)
        amm2 = Amenity()
        self.assertLess(amm1.updated_at, amm2.updated_at)

    def test_two_amenities_different_created_at(self):
        amm1 = Amenity()
        sleep(0.05)
        amm2 = Amenity()
        self.assertLess(amm1.created_at, amm2.created_at)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests that tests save method of the Amenity class."""

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

    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def test_two_saves(self):
        amm = Amenity()
        sleep(0.05)
        first_updated_at = amm.updated_at
        amm.save()
        second_updated_at = amm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amm.save()
        self.assertLess(second_updated_at, amm.updated_at)


    def test_one_save(self):
        amm = Amenity()
        sleep(0.05)
        first_updated_at = amm.updated_at
        amm.save()
        self.assertLess(first_updated_at, amm.updated_at)

    def test_save_updates_file(self):
        amm = Amenity()
        amm.save()
        ammid = "Amenity." + amm.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())

    def test_save_with_arg(self):
        amm = Amenity()
        with self.assertRaises(TypeError):
            amm.save(None)

class TestAmenity_to_dict(unittest.TestCase):
    """Unittest for testing to_dict method of Amenity class."""
    def test_to_dict_contains_correct_keys(self):
        amm = Amenity()
        self.assertIn("id", amm.to_dict())
        self.assertIn("created_at", amm.to_dict())
        self.assertIn("updated_at", amm.to_dict())
        self.assertIn("__class__", amm.to_dict())

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))


    def test_to_dict_datetime_attributes_are_strs(self):
        amm = Amenity()
        amm_dict = amm.to_dict()
        self.assertEqual(str, type(amm_dict["id"]))
        self.assertEqual(str, type(amm_dict["created_at"]))
        self.assertEqual(str, type(amm_dict["updated_at"]))

    def test_to_dict_contains_added_attributes(self):
        amm = Amenity()
        amm.middle_name = "Holberton"
        amm.my_number = 98
        self.assertEqual("Holberton", amm.middle_name)
        self.assertIn("my_number", amm.to_dict())

    def test_to_dict_output(self):
        dt = datetime.today()
        amm = Amenity()
        amm.id = "123456"
        amm.created_at = amm.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(amm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        amm = Amenity()
        self.assertNotEqual(amm.to_dict(), amm.__dict__)

    def test_to_dict_with_arg(self):
        amm = Amenity()
        with self.assertRaises(TypeError):
            amm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
