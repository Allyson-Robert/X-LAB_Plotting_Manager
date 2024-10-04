"""
    This util tool should be used to sanitize datetime strings across data files from a variety of sources.
    It should be able to deal with any format that is explicitly specified, such as

    YYYY_MM_DD
    YYYY_MM_DD-HH_MM_SS

    Including any variation using different types of change in the use of - or _ as I am very inconsitent in the uses
"""
import re
from datetime import datetime
import unittest


class CustomDatetime:
    """
    A utility class to sanitize and handle datetime strings across data files from a variety of sources.
    It can deal with any format explicitly specified and convert it to a consistent format.
    Default formats are provided

    Attributes:
        separators (str): Possible separator symbols in the datetime strings.
        label_format (str): Desired default label format for datetime strings.
        default_time (str): Default time to use if no time is found in the input string.
        date_pattern (str): Regex pattern to match date parts in the input string, use 0 for separators.
        time_pattern (str): Regex pattern to match time parts in the input string, use 0 for separators.
    """
    # TODO: Make this readable from a config file

    def __init__(self,
                 separators="-_",
                 label_format="%Y_%m_%d_%H_%M_%S",
                 default_time="09_00_00",
                 date_pattern=r'(\d{{4}})[{0}](\d{{2}})[{0}](\d{{2}})',
                 time_pattern=r'(\d{{2}})[{0}](\d{{2}})[{0}](\d{{2}})'):

        # Possible separator symbols
        self.separators = separators

        # Desired default label
        self.label_format = label_format
        self.default_time = default_time

        # Patterns to match date and time separately
        self.date_pattern = date_pattern.format(self.separators)
        self.time_pattern = time_pattern.format(self.separators)

    def create_datetime_from_string(self, input_datetime_str: str = None) -> datetime:
        """
        Creates a datetime object from an input datetime string.

        Args:
            input_datetime_str (str): The input datetime string.

        Returns:
            datetime: The resulting datetime object.

        Raises:
            ValueError: If the input string is None or does not contain a valid date.
        """
        if input_datetime_str is None:
            raise ValueError("Input datetime string cannot be None")

        # Search for date in string using pattern
        date_match = re.search(self.date_pattern, input_datetime_str)
        if not date_match:
            raise ValueError("Input string does not contain a valid date")

        date_str = re.sub(fr'[{self.separators}]', '_', date_match.group())

        # Remove the date part from the original string to search for the time part
        remaining_str = input_datetime_str[date_match.end():]

        # Search for time in string using pattern
        time_match = re.search(self.time_pattern, remaining_str)
        if time_match:
            time_str = re.sub(fr'[{self.separators}]', '_', time_match.group())
        else:
            # Use default time if not found
            time_str = self.default_time

        # Combine date and time
        datetime_str = f"{date_str}_{time_str}"

        # Convert to datetime object
        datetime_obj = datetime.strptime(datetime_str, self.label_format)
        return datetime_obj

    def write_datetime_to_string(self, input_datetime: datetime = None) -> str:
        """
        Converts a datetime object to a formatted string.

        Args:
            input_datetime (datetime): The input datetime object.

        Returns:
            str: The resulting formatted datetime string.

        Raises:
            ValueError: If the input datetime object is None.
        """
        if input_datetime is None:
            raise ValueError("Input datetime cannot be None")

        # Convert datetime object to string
        datetime_str = input_datetime.strftime(self.label_format)
        return datetime_str


class TestCustomDatetime(unittest.TestCase):

    def test_create_datetime_from_string_with_default_time(self):
        sanitizer = CustomDatetime()
        test_datetime_str = "2024-06-14"
        dt_obj = sanitizer.create_datetime_from_string(test_datetime_str)
        expected_datetime = datetime(2024, 6, 14, 9, 0, 0)
        self.assertEqual(dt_obj, expected_datetime)

    def test_create_datetime_from_string_with_time(self):
        sanitizer = CustomDatetime()
        test_datetime_str = "2024-06-14-12_30_45"
        dt_obj = sanitizer.create_datetime_from_string(test_datetime_str)
        expected_datetime = datetime(2024, 6, 14, 12, 30, 45)
        self.assertEqual(dt_obj, expected_datetime)

    def test_write_datetime_to_string(self):
        sanitizer = CustomDatetime()
        test_datetime_obj = datetime(2024, 6, 14, 12, 30, 45)
        dt_str = sanitizer.write_datetime_to_string(test_datetime_obj)
        expected_str = "2024_06_14_12_30_45"
        self.assertEqual(dt_str, expected_str)

    def test_custom_separator(self):
        sanitizer = CustomDatetime(separators="/-")
        test_datetime_str = "2024/06/14-12/30/45"
        dt_obj = sanitizer.create_datetime_from_string(test_datetime_str)
        expected_datetime = datetime(2024, 6, 14, 12, 30, 45)
        self.assertEqual(dt_obj, expected_datetime)

    def test_invalid_date_string(self):
        sanitizer = CustomDatetime()
        with self.assertRaises(ValueError):
            sanitizer.create_datetime_from_string("2024/06/14 12:30:45")

    def test_none_datetime_string(self):
        sanitizer = CustomDatetime()
        with self.assertRaises(ValueError):
            sanitizer.create_datetime_from_string(None)

    def test_none_datetime_object(self):
        sanitizer = CustomDatetime()
        with self.assertRaises(ValueError):
            sanitizer.write_datetime_to_string(None)


if __name__ == "__main__":
    unittest.main()