import unittest
import os, shutil
from datetime import datetime
from dataspec_manager.dataspec import DataSpec  # Assuming the class is defined in a file named dataspec.py

class TestDataSpec(unittest.TestCase):
    def setUp(self):
        # Initialize a DataSpec object for testing
        self.data_spec = DataSpec(creation_date="2024.12.25_00.00.00")

    def test_initialization(self):
        self.assertEqual(self.data_spec.get_creation_date(),
                         datetime.strptime("2024.12.25_00.00.00", "%Y.%m.%d_%H.%M.%S"))

    def test_name_methods(self):
        self.data_spec.set_name("Experiment1")
        self.assertEqual(self.data_spec.get_name(), "Experiment1")

    def test_experiment_date_methods(self):
        self.data_spec.set_experiment_date("2024.12.26_15.30.00")
        self.assertEqual(self.data_spec.get_experiment_date(),
                         datetime.strptime("2024.12.26_15.30.00", "%Y.%m.%d_%H.%M.%S"))

    def test_device_methods(self):
        self.data_spec.set_device("DeviceA")
        self.assertEqual(self.data_spec.get_device(), "DeviceA")

    def test_structure_type_methods(self):
        self.data_spec.set_structure_type("structured")
        self.assertEqual(self.data_spec.get_structure_type(), "structured")
        with self.assertRaises(ValueError):
            self.data_spec.set_structure_type("invalid_type")

    def test_notes_methods(self):
        self.data_spec.set_notes("Initial notes")
        self.assertEqual(self.data_spec.get_notes(), "Initial notes")
        self.data_spec.add_notes(" Additional notes.")
        self.assertEqual(self.data_spec.get_notes(), "Initial notes Additional notes.")

    def test_console_methods(self):
        console_data = {"2024-12-25 12:00:00": "Console entry 1"}
        self.data_spec.set_console(console_data)
        self.assertEqual(self.data_spec.get_console(), console_data)
        self.data_spec.add_console("2024-12-26 14:00:00", "Console entry 2")
        self.assertIn("2024-12-26 14:00:00", self.data_spec.get_console())

    def test_filepaths_methods(self):
        try:
            # Create file
            temp_file_name = "file1.txt"
            with open(temp_file_name, "w") as temp_file:
                temp_file.write("temporary content")

            # Add file and check filepaths
            self.data_spec.add_filepath(temp_file_name, "file1")
            self.data_spec.get_filepaths()
            self.assertEqual(self.data_spec.get_filepath("file1"), temp_file_name)
            with self.assertRaises(KeyError):
                self.data_spec.get_filepath("nonexistent")
        finally:
            # Remove file
            if os.path.exists(temp_file_name):
                os.remove(temp_file_name)

    def test_colours_methods(self):
        self.data_spec.add_colour("#FF5733", "highlight")
        self.assertEqual(self.data_spec.get_single_colour("highlight"), "#FF5733")
        self.assertIsNone(self.data_spec.get_single_colour("nonexistent"))

    def test_path_validation(self):
        # Setup for testing
        temp_file_name = "temp_test_file.txt"
        temp_dir_name = "temp_test_dir"
        invalid_file_name = "temp_test_file.invalid"

        try:
            # Valid file test
            with open(temp_file_name, "w") as temp_file:
                temp_file.write("temporary content")
            is_valid, message = self.data_spec._check_valid_path(temp_file_name)
            self.assertTrue(is_valid)
            self.assertEqual(message, "")

            # Incorrect file extension test
            with open(invalid_file_name, "w") as invalid_file:
                invalid_file.write("temporary content")
            is_valid, message = self.data_spec._check_valid_path(invalid_file_name)
            self.assertFalse(is_valid)
            self.assertIn("Forbidden Extension", message)

            # Path is not a file test
            os.mkdir(temp_dir_name)
            is_valid, message = self.data_spec._check_valid_path(temp_dir_name)
            self.assertFalse(is_valid)
            self.assertIn("Not a File", message)

            # Nonexistent file test
            nonexistent_file = "nonexistent_file.txt"
            is_valid, message = self.data_spec._check_valid_path(nonexistent_file)
            self.assertFalse(is_valid)
            self.assertIn("Filesystem Error", message)
        finally:
            # Cleanup
            if os.path.exists(temp_file_name):
                os.remove(temp_file_name)
            if os.path.exists(invalid_file_name):
                os.remove(invalid_file_name)
            if os.path.exists(temp_dir_name):
                os.rmdir(temp_dir_name)

    def test_flat_filepaths_construction(self):
        try:
            # Prepare files and directories
            root_dir = "/home/allyson/Downloads"
            temp_files = [
                (f"{root_dir}/file1.txt", "file1"),
                (f"{root_dir}/file2.csv", "file2"),
                (f"{root_dir}/file3.invalid", "file3")  # Not an allowed extension
            ]

            # Create the files for the test
            for file_name, _ in temp_files:
                with open(file_name, "w") as f:
                    f.write("temporary content")

            # Test flat structure construction
            self.data_spec.construct_filepaths(root_dir, type="flat")
            constructed_paths_flat = self.data_spec.get_filepaths()

            # Validate flat structure results
            self.assertIn(f"file1", constructed_paths_flat)
            self.assertIn(f"file2", constructed_paths_flat)
            self.assertNotIn(f"file3", constructed_paths_flat)  # Should be excluded
            self.assertIsInstance(self.data_spec.filepaths, dict)
            self.assertEqual(self.data_spec.filepaths.get("file1"), f"{root_dir}/file1.txt")
            self.assertEqual(self.data_spec.filepaths.get("file2"), f"{root_dir}/file2.csv")
            self.assertNotIn("file3", self.data_spec.filepaths)

        finally:
            for file_name, _ in temp_files:
                try:
                    os.remove(os.path.join(root_dir, file_name))
                except FileNotFoundError:
                    pass

    def test_structured_filepaths_construction(self):
        try:
            root_dir = "/home/allyson/Downloads"
            os.makedirs(os.path.join(root_dir, "level1", "level2a", "level3"), exist_ok=True)
            os.makedirs(os.path.join(root_dir, "level1", "level2b"), exist_ok=True)

            # Files in level2a
            nested_file1 = os.path.join("level1", "level2a", "file1.csv")
            nested_file4 = os.path.join("level1", "level2a", "file4.txt")
            unsupported_file1 = os.path.join("level1", "level2a", "file4.invalid")

            # Files in level 3
            nested_file2 = os.path.join("level1", "level2a", "level3", "file2.txt")
            nested_file3 = os.path.join("level1", "level2a", "level3", "file3.txt")
            unsupported_file3 = os.path.join("level1", "level2a", "level3", "file3.invalid")

            # Files in level2b
            nested_file5 = os.path.join("level1", "level2b", "file5.txt")
            unsupported_file2 = os.path.join("level1", "level2b", "file5.invalid")

            # Files in level1
            level1_file1 = os.path.join("level1", "file6.txt")
            unsupported_level1_file = os.path.join("level1", "file6.invalid")

            # Create the files
            for file_path in [nested_file1, nested_file2, nested_file3, nested_file4, nested_file5, level1_file1]:
                with open(os.path.join(root_dir, file_path), "w") as f:
                    f.write("temporary content")
            for file_path in [unsupported_file1, unsupported_file2, unsupported_file3, unsupported_level1_file]:
                with open(os.path.join(root_dir, file_path), "w") as f:
                    f.write("unsupported content")

            # Call the filepath construction method
            self.data_spec.construct_filepaths(f"{root_dir}/level1", type="structured")
            constructed_paths_nested = self.data_spec.get_filepaths()

            # Validate nested structure results
            expected_filepaths = {
                'level2a': {
                    'file1.csv': '/home/allyson/Downloads/level1/level2a/file1.csv',
                    'file4.txt': '/home/allyson/Downloads/level1/level2a/file4.txt'
                }, 'level2b': {
                    'file5.txt': '/home/allyson/Downloads/level1/level2b/file5.txt'
                }
            }
            # Validate the entire structure
            self.assertEqual(constructed_paths_nested, expected_filepaths)

        finally:
            # Cleanup: remove created files and directories
            shutil.rmtree(os.path.join(root_dir, "level1"), ignore_errors=True)

    def test_equality(self):
        other_data_spec = DataSpec(creation_date="2024.12.25_00.00.00")
        self.assertEqual(self.data_spec, other_data_spec)
        other_data_spec.set_name("DifferentName")
        self.assertNotEqual(self.data_spec, other_data_spec)

if __name__ == "__main__":
    unittest.main()
