import hashlib

import pandas as pd

from src.schema import CANONICAL_COLUMNS
from src.validation import apply_pandas_validations


def transform_records(records):
    df = pd.DataFrame(records)

    if df.empty:
        empty_valid = pd.DataFrame(columns=CANONICAL_COLUMNS)
        empty_invalid = pd.DataFrame(columns=CANONICAL_COLUMNS + ["validation_errors", "ingestion_ts"])
        return empty_valid, empty_invalid

    df["flight_id"] = df.apply(
        lambda row: hashlib.sha256(
            f"{row.get('airline')}_{row.get('flight_number')}_{row.get('flight_date')}".encode()
        ).hexdigest(),
        axis=1,
    )

    return apply_pandas_validations(df)
