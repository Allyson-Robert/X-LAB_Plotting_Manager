import csv
import pandas as pd
from io import StringIO


def read_csv(path, skip_lines=0, delimiter=None) -> list:
    """
    Reads tabular measurement or CSV data.

    - Handles tab/space-separated files.
    - Stops at 'end data' if present.
    - Returns a list of columns (lists).
    - If metadata exists after 'end data', it's appended as a dict.
    """

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Split into data and metadata parts ---
    content_lower = content.lower()
    meta_dict = {}

    if "end data" in content_lower:
        data_part, meta_part = content.split("end data", 1)
        lines = [line for line in data_part.splitlines() if line.strip()]

        # Parse metadata into dict
        for line in meta_part.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                meta_dict[key.strip()] = value.strip()
    else:
        # No "end data" marker, just use whole file
        lines = [line for line in content.splitlines() if line.strip()]

    # --- Read data ---
    try:
        df = pd.read_csv(
            StringIO("\n".join(lines)),
            delim_whitespace=True,
            na_values=["NaN"],
            skiprows=skip_lines,
            engine="python",
        )
    except Exception:
        # Fallback: use csv.reader if pandas parsing fails
        if delimiter is None:
            with open(path) as csvfile:
                sample = csvfile.read(2048)
                try:
                    dialect = csv.Sniffer().sniff(sample)
                    delimiter = dialect.delimiter
                except csv.Error:
                    delimiter = ','

        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            for _ in range(skip_lines):
                next(reader, None)
            rows = [r for r in reader if len(r) > 0]
        df = pd.DataFrame(rows)

    # --- Clean and convert data ---
    data_columns = []
    for col in df.columns:
        series = df[col]
        try:
            # Convert numeric strings safely
            converted = pd.to_numeric(series.astype(str).str.replace(',', '.'), errors='ignore')
        except Exception:
            converted = series
        data_columns.append(converted.tolist())

    # --- Append metadata if any ---
    if meta_dict:
        data_columns.append(meta_dict)

    return data_columns
