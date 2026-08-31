from src.pandas_pipeline.transform import transform_records
from tests.fixtures.sample_flights import SAMPLE_FLIGHTS_MIXED


def test_transform_pandas_quarantines_invalid_rows():
    valid_df, invalid_df = transform_records(SAMPLE_FLIGHTS_MIXED)

    assert len(valid_df) == 1
    assert len(invalid_df) == 2
    assert "validation_errors" in invalid_df.columns
    assert invalid_df["validation_errors"].str.contains("arrival_before_departure").any()
    assert invalid_df["validation_errors"].str.contains("missing_flight_number").any()
