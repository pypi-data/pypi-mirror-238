import unittest

from src.wslconv.wslconv import WSLPathConverter


class TestWSLPathConverter(unittest.TestCase):

    def setUp(self):
        self.expected_results = {
            "to_linux": [
                "/home/username/file.txt",
                "/mnt/c/Users/username/file.txt",
                "/home/username/file.txt",
                "/mnt/c/Users/username/file.txt",
                "/mnt/c/Users/username/file.txt"
            ],
            "to_windows": [
                "\\\\wsl.localhost\\Debian\\home\\username\\file.txt",
                "C:\\Users\\username\\file.txt",
                "\\\\wsl.localhost\\Debian\\home\\username\\file.txt",
                "C:\\Users\\username\\file.txt",
                "C:\\Users\\username\\file.txt"
            ],
            "os_type": ["Linux", "Linux", "Windows", "Windows", "Windows"],
            "filesystem_type": ["Linux", "Windows", "Linux", "Windows", "Windows"]
        }

        self.paths = [
            "/home/username/file.txt",
            "/mnt/c/Users/username/file.txt",
            "\\\\wsl.localhost\\Debian\\home\\username\\file.txt",
            "C:\\Users\\username\\file.txt",
            "\\\\wsl.localhost\\Debian\\mnt\\c\\Users\\username\\file.txt"
        ]

    def test_path_conversion(self):
        for method, expected_values in self.expected_results.items():
            for path, expected in zip(self.paths, expected_values):
                with self.subTest(method=method, path=path):
                    converter = WSLPathConverter(path, "Debian")
                    actual = getattr(converter, method)()
                    self.assertEqual(actual, expected,
                                     f"For path '{path}', method '{method}' returned '{actual}', expected '{expected}'")


if __name__ == "__main__":
    unittest.main()
