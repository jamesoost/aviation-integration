from pyspark.sql import functions as F

from src.validation import apply_spark_validations


def transform_records(spark, records):
    spark_df = spark.createDataFrame(records)

    if "flight_id" not in spark_df.columns:
        spark_df = spark_df.withColumn(
            "flight_id",
            F.sha2(
                F.concat_ws(
                    "_",
                    F.coalesce(F.col("airline"), F.lit("")),
                    F.coalesce(F.col("flight_number"), F.lit("")),
                    F.coalesce(F.col("flight_date"), F.lit("")),
                ),
                256,
            ),
        )

    return apply_spark_validations(spark_df)
