import unittest
from brams import systems, files

class TestFiles(unittest.TestCase):

    def test_get_valid_file_start(self):

        f = files.get("2023-10-01T00:00", "BEHUMA_SYS001")
        self.assertIsInstance(f, files.File)

        s = systems.get("BEHUMA_SYS001")
        f = files.get("2023-10-01T00:00", s)
        self.assertIsInstance(f, files.File)

        s = systems.get(location = "BEHUMA")
        f = files.get("2023-10-01T00:00", list(s.keys()))

        self.assertIsInstance(f, dict)
        
        for key, value in f.items():

            self.assertIsInstance(key, str)
            self.assertIsInstance(value, files.File)

        f = files.get("2023-10-01T00:00", list(s.values()))
        self.assertIsInstance(f, dict)
        
        for key, value in f.items():

            self.assertIsInstance(key, str)
            self.assertIsInstance(value, files.File)

        f = files.get("2023-10-01T00:00", s)
        self.assertIsInstance(f, dict)
        
        for key, value in f.items():

            self.assertIsInstance(key, str)
            self.assertIsInstance(value, files.File)


    def test_get_valid_file_interval(self):

        f = files.get("2023-10-01T00:00/2023-10-01T00:20", "BEHUMA_SYS001")
        self.assertIsInstance(f, dict)

        for key, value in f.items():

            self.assertIsInstance(key, str)
            self.assertIsInstance(value, list)

            for element in value:

                self.assertIsInstance(element, files.File)

        s = systems.get("BEHUMA_SYS001")
        f = files.get("2023-10-01T00:00/2023-10-01T00:20", s)
        self.assertIsInstance(f, dict)
        
        for key, value in f.items():

            self.assertIsInstance(key, str)
            self.assertIsInstance(value, list)

            for element in value:

                self.assertIsInstance(element, files.File)

        s = systems.get(location = "BEHUMA")
        f = files.get("2023-10-01T00:00/2023-10-01T00:20", s.keys())
        self.assertIsInstance(f, dict)
        
        for key, value in f.items():

            self.assertIsInstance(key, str)
            self.assertIsInstance(value, list)

            for element in value:

                self.assertIsInstance(element, files.File)


        f = files.get("2023-10-01T00:00/2023-10-01T00:20", s.values())
        self.assertIsInstance(f, dict)
        
        for key, value in f.items():

            self.assertIsInstance(key, str)
            self.assertIsInstance(value, list)

            for element in value:

                self.assertIsInstance(element, files.File)

        f = files.get("2023-10-01T00:00/2023-10-01T00:20", s)
        self.assertIsInstance(f, dict)
        
        for key, value in f.items():

            self.assertIsInstance(key, str)
            self.assertIsInstance(value, list)

            for element in value:

                self.assertIsInstance(element, files.File)


    def test_get_invalid_file(self):

        f = files.get("INVALID", "INVALID")
        self.assertIsNone(f)

if __name__ == '__main__':
    
    unittest.main()