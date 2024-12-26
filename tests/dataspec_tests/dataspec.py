import unittest
import os
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
        self.data_spec.add_filepath("/path/to/file1.txt", "file1")
        self.assertEqual(self.data_spec.get_filepath("file1"), "/path/to/file1.txt")
        with self.assertRaises(KeyError):
            self.data_spec.get_filepath("nonexistent")

    def test_colours_methods(self):
        self.data_spec.add_colour("#FF5733", "highlight")
        self.assertEqual(self.data_spec.get_single_colour("highlight"), "#FF5733")
        with self.assertRaises(KeyError):
            self.data_spec.get_single_colour("nonexistent")

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

    def test_filepaths_construction(self):
        root_dir = "/home/allyson/Downloads"

        # Prepare files and directories
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
        for file_name, label in temp_files:
            self.data_spec.add_filepath(path=file_name, label=label)

        constructed_paths_flat = self.data_spec.get_filepaths()
        print(constructed_paths_flat)

        # Validate flat structure results
        self.assertIn(f"file1", constructed_paths_flat)
        self.assertIn(f"file2", constructed_paths_flat)
        self.assertNotIn(f"file3", constructed_paths_flat)  # Should be excluded
        self.assertIsInstance(self.data_spec.filepaths, dict)
        self.assertEqual(self.data_spec.filepaths.get("file1"), f"{root_dir}/file1.txt")
        self.assertEqual(self.data_spec.filepaths.get("file2"), f"{root_dir}/file2.csv")
        self.assertNotIn("file3", self.data_spec.filepaths)  # Should not exist in filepaths

        # Test nested structure construction
        self.data_spec.filepaths = {}  # Reset to ensure clean state
        nested_files = [
            ("nested_dir/file4.txt", "nested.file4"),
            ("nested_dir/file5.invalid", "nested.file5")  # Not an allowed extension
        ]

        # Create the nested files for the test
        os.makedirs(os.path.join(root_dir, "nested_dir"), exist_ok=True)
        for file_name, _ in nested_files:
            with open(os.path.join(root_dir, file_name), "w") as f:
                f.write("temporary content")

        for file_name, _ in nested_files:
            self.data_spec.add_filepath(file_name, file_name)

        constructed_paths_nested = self.data_spec.construct_filepaths(root_dir)

        # Validate nested structure results
        self.assertIn(f"{root_dir}/nested_dir/file4.txt", constructed_paths_nested)
        self.assertNotIn(f"{root_dir}/nested_dir/file5.invalid", constructed_paths_nested)  # Should be excluded
        self.assertIsInstance(self.data_spec.filepaths, dict)
        self.assertIn("nested", self.data_spec.filepaths)
        self.assertIsInstance(self.data_spec.filepaths["nested"], dict)
        self.assertEqual(self.data_spec.filepaths["nested"].get("file4"), f"{root_dir}/nested_dir/file4.txt")
        self.assertNotIn("file5", self.data_spec.filepaths["nested"])  # Should not exist in filepaths

        # Cleanup: remove created files and directories
        for file_name, _ in temp_files + nested_files:
            try:
                os.remove(os.path.join(root_dir, file_name))
            except FileNotFoundError:
                pass
        os.rmdir(os.path.join(root_dir, "nested_dir"))

    def test_equality(self):
        other_data_spec = DataSpec(creation_date="2024.12.25_00.00.00")
        self.assertEqual(self.data_spec, other_data_spec)
        other_data_spec.set_name("DifferentName")
        self.assertNotEqual(self.data_spec, other_data_spec)

if __name__ == "__main__":
    unittest.main()
