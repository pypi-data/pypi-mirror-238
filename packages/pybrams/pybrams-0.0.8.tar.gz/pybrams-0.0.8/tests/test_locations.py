import unittest
from brams import locations

class TestLocations(unittest.TestCase):

    def test_get_valid_location(self):

        # Test the 'get' function with a valid location_code (BEHUMA)
        location = locations.get("BEHUMA")
        self.assertIsInstance(location, locations.Location)
        self.assertEqual(location.location_code, "BEHUMA")
        self.assertIsInstance(location.location_code, str)
        self.assertIsInstance(location.name, str)
        self.assertIsInstance(location.status, str)
        self.assertIsInstance(location.longitude, float)
        self.assertIsInstance(location.latitude, float)
        self.assertIsInstance(location.altitude, float)
        self.assertIsInstance(location.systems_url, str)

    def test_get_invalid_location(self):

        location = locations.get("INVALID")
        self.assertIsNone(location)

    def test_all_returns_dict(self):

        locations_dict = locations.all()
        self.assertIsInstance(locations_dict, dict)

    def test_all_contains_locations(self):

        locations_dict = locations.all()
        self.assertIn("BEHUMA", locations_dict)
        # Add more assertions to check other location codes as needed.

if __name__ == '__main__':
    
    unittest.main()