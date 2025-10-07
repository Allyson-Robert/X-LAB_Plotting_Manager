import re
from datetime import datetime
import unittest


class CustomDatetime:
    def __init__(self,
                 separators="-_",
                 label_format="%Y_%m_%d_%H_%M_%S",
                 default_time="09_00_00",
                 date_pattern=None,
                 time_pattern=None):

        self.separators = separators
        self.label_format = label_format
        self.default_time = default_time

        # If user didn't pass custom patterns, use default YYYY_MM_DD / HH_MM_SS
        self.date_pattern = date_pattern or rf"(\d{{4}})[{self.separators}](\d{{2}})[{self.separators}](\d{{2}})"
        self.time_pattern = time_pattern or rf"(\d{{2}})[{self.separators}](\d{{2}})[{self.separators}](\d{{2}})"

    def create_datetime_from_string(self, input_datetime_str: str = None) -> datetime:
        """
        Creates a datetime object from an input datetime string.

        - Infers %Y vs %y from the year token length.
        - Allows HH_MM or HH_MM_SS; pads seconds to 00 when missing.
        """
        if input_datetime_str is None:
            raise ValueError("Input datetime string cannot be None")

        # --- Find date ---
        date_match = re.search(self.date_pattern, input_datetime_str)
        if not date_match:
            raise ValueError(f"Input string {input_datetime_str} does not contain a valid date")

        date_groups = date_match.groups()
        if len(date_groups) != 3:
            raise ValueError("Date pattern must capture exactly 3 groups (Y, m, d)")

        year_token = date_groups[0]
        if len(year_token) == 4:
            date_fmt = "%Y_%m_%d"
        elif len(year_token) == 2:
            date_fmt = "%y_%m_%d"
        else:
            raise ValueError("Year group must be 2 or 4 digits")

        date_str = "_".join(date_groups)

        # --- Find time (search only after date to avoid picking up pre-date tokens) ---
        remaining_str = input_datetime_str[date_match.end():]
        time_match = re.search(self.time_pattern, remaining_str)

        if time_match:
            time_groups = time_match.groups()
            if len(time_groups) == 3:
                time_str = "_".join(time_groups)  # HH_MM_SS
                time_fmt = "%H_%M_%S"
            elif len(time_groups) == 2:
                time_str = f"{time_groups[0]}_{time_groups[1]}_00"  # HH_MM_00
                time_fmt = "%H_%M_%S"
            else:
                raise ValueError("Time pattern must capture 2 (H,M) or 3 (H,M,S) groups")
        else:
            # Use default time (assumed HH_MM_SS like "09_00_00")
            time_str = self.default_time
            time_fmt = "%H_%M_%S"

        # Final assemble + parse
        datetime_str = f"{date_str}_{time_str}"
        fmt = f"{date_fmt}_{time_fmt}"
        return datetime.strptime(datetime_str, fmt)

    def write_datetime_to_string(self, input_datetime: datetime) -> str:
        if input_datetime is None:
            raise ValueError("Input datetime cannot be None")
        return input_datetime.strftime(self.label_format)


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

    def test_compact_pattern_yymmdd_hhmm(self):
        """
        Should parse 'QE 250812-1332 IXYS-UV1' as 2025-08-12 13:32:00.
        Date = YYMMDD, Time = HHMM (seconds default to 00).
        """
        sanitizer = CustomDatetime(
            date_pattern=r"(\d{2})(\d{2})(\d{2})",  # YY MM DD
            time_pattern=r"(\d{2})(\d{2})"          # HH MM (no seconds)
        )
        test_datetime_str = "QE 250812-1332 IXYS-UV1"
        dt_obj = sanitizer.create_datetime_from_string(test_datetime_str)
        expected_datetime = datetime(2025, 8, 12, 13, 32, 0)
        self.assertEqual(dt_obj, expected_datetime)

    def test_compact_pattern_appearing_anywhere(self):
        """
        The compact pattern should be found even if surrounded by other tokens,
        and still default seconds to 00.
        """
        sanitizer = CustomDatetime(
            date_pattern=r"(\d{2})(\d{2})(\d{2})",  # YY MM DD
            time_pattern=r"(\d{2})(\d{2})"          # HH MM
        )
        test_datetime_str = "prefix-QE 250812-1332-IXYS-UV1-suffix"
        dt_obj = sanitizer.create_datetime_from_string(test_datetime_str)
        expected_datetime = datetime(2025, 8, 12, 13, 32, 0)
        self.assertEqual(dt_obj, expected_datetime)


if __name__ == "__main__":
    unittest.main()