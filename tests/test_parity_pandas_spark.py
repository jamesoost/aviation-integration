import pytest
import pandas as pd

from src.schema import CANONICAL_COLUMNS
from src.pandas_pipeline.transform import transform_records as transform_pandas_records
from src.pyspark_pipeline.transform import transform_records as transform_spark_records
from tests.fixtures.sample_flights import SAMPLE_FLIGHTS_MIXED


def test_pandas_spark_parity_columns_and_valid_count():
    pyspark = pytest.importorskip("pyspark")

    pandas_valid, pandas_invalid = transform_pandas_records(SAMPLE_FLIGHTS_MIXED)

    spark = pyspark.sql.SparkSession.builder.appName("test-parity").master("local[1]").getOrCreate()
    try:
        spark_valid, spark_invalid = transform_spark_records(spark, SAMPLE_FLIGHTS_MIXED)
        spark_valid_pd = pd.DataFrame([row.asDict(recursive=True) for row in spark_valid.collect()])
        spark_invalid_pd = pd.DataFrame([row.asDict(recursive=True) for row in spark_invalid.collect()])
    finally:
        spark.stop()

    assert list(pandas_valid.columns) == CANONICAL_COLUMNS
    assert list(spark_valid_pd.columns) == CANONICAL_COLUMNS
    assert list(pandas_invalid.columns) == CANONICAL_COLUMNS + ["validation_errors", "ingestion_ts"]
    assert list(spark_invalid_pd.columns) == CANONICAL_COLUMNS + ["validation_errors", "ingestion_ts"]
    assert len(pandas_valid) == len(spark_valid_pd)
    assert len(pandas_invalid) == len(spark_invalid_pd)

    pandas_errors = set(pandas_invalid["validation_errors"].tolist())
    spark_errors = set(spark_invalid_pd["validation_errors"].tolist())
    assert pandas_errors == spark_errors
