from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

try:
    from .schema import CANONICAL_COLUMNS, DATETIME_FIELDS, REQUIRED_FIELDS
except ImportError:
    from schema import CANONICAL_COLUMNS, DATETIME_FIELDS, REQUIRED_FIELDS


def apply_pandas_validations(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    working_df = df.copy()

    for field in DATETIME_FIELDS:
        working_df[field] = pd.to_datetime(working_df[field], errors="coerce", utc=True)

    errors = pd.Series("", index=working_df.index, dtype="object")

    for field in REQUIRED_FIELDS:
        missing = working_df[field].isna() | (working_df[field].astype("string").str.strip() == "")
        errors = errors.mask(missing, errors + f"missing_{field};")

    datetime_parse_fail = working_df[DATETIME_FIELDS].isna().any(axis=1)
    errors = errors.mask(datetime_parse_fail, errors + "invalid_datetime;")

    arrival_before_departure = (
        working_df["scheduled_arrival_time"] < working_df["scheduled_departure_time"]
    )
    errors = errors.mask(arrival_before_departure, errors + "arrival_before_departure;")

    working_df["validation_errors"] = errors.str.rstrip(";")
    working_df["ingestion_ts"] = datetime.now(timezone.utc).isoformat()

    invalid_mask = working_df["validation_errors"] != ""
    invalid_df = working_df[invalid_mask].copy()
    valid_df = working_df[~invalid_mask].copy()

    return valid_df[CANONICAL_COLUMNS], invalid_df[CANONICAL_COLUMNS + ["validation_errors", "ingestion_ts"]]


def apply_spark_validations(df):
    from pyspark.sql import functions as F

    working_df = (
        df.withColumn("scheduled_departure_time", F.to_timestamp("scheduled_departure_time"))
        .withColumn("scheduled_arrival_time", F.to_timestamp("scheduled_arrival_time"))
    )

    error_parts = []

    for field in REQUIRED_FIELDS:
        error_parts.append(
            F.when(
                F.col(field).isNull() | (F.trim(F.col(field)) == ""),
                F.lit(f"missing_{field}"),
            )
        )

    error_parts.append(
        F.when(
            F.col("scheduled_departure_time").isNull() | F.col("scheduled_arrival_time").isNull(),
            F.lit("invalid_datetime"),
        )
    )

    error_parts.append(
        F.when(
            F.col("scheduled_arrival_time") < F.col("scheduled_departure_time"),
            F.lit("arrival_before_departure"),
        )
    )

    working_df = working_df.withColumn(
        "validation_errors",
        F.concat_ws(";", *error_parts),
    ).withColumn("ingestion_ts", F.current_timestamp())

    invalid_df = working_df.filter(F.col("validation_errors") != "")
    valid_df = working_df.filter(F.col("validation_errors") == "")

    return valid_df.select(*CANONICAL_COLUMNS), invalid_df.select(
        *(CANONICAL_COLUMNS + ["validation_errors", "ingestion_ts"])
    )
