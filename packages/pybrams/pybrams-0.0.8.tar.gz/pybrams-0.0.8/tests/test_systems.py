import unittest
from brams import systems
from brams import locations

class TestSystems(unittest.TestCase):

    def test_get_system_by_location(self):

        location = locations.get("BEBILZ")
        system = systems.get(location=location)
        self.assertIsInstance(system, systems.System)
        self.assertIsInstance(system.system_code, str)
        self.assertIsInstance(system.name, str)
        self.assertIsInstance(system.start, str)
        self.assertIsInstance(system.end, str)
        self.assertIsInstance(system.antenna, int)
        self.assertIsInstance(system.location_url, str)
        self.assertIsInstance(system.location_code, str)

        location = locations.get("BEHUMA")
        system = systems.get(location=location)
        self.assertIsInstance(system, dict)        

    def test_get_system_by_system_code(self):

        system = systems.get(system_code="BEHUMA_SYS001") 
        self.assertIsInstance(system, systems.System)
        self.assertIsInstance(system.system_code, str)
        self.assertIsInstance(system.name, str)
        self.assertIsInstance(system.start, str)
        self.assertIsInstance(system.end, str)
        self.assertIsInstance(system.antenna, int)
        self.assertIsInstance(system.location_url, str)
        self.assertIsInstance(system.location_code, str)

    def test_get_invalid_system(self):

        system = systems.get(system_code="INVALID")
        self.assertIsNone(system)
        system = systems.get(location=None)
        self.assertIsNone(system)

    def test_all_contains_systems(self):

        systems_dict = systems.all()
        expected_system_codes = ["BEHUMA_SYS001", "BEHUMA_SYS002", "BEHUMA_SYS003", "BEHUMA_SYS004", "BEHUMA_SYS005", "BEHUMA_SYS006"]

        for system_code in expected_system_codes:

            self.assertIn(system_code, systems_dict)

if __name__ == '__main__':

    unittest.main()