import argparse

from src.pipeline import run_extract_step, run_load_step, run_pipeline, run_transform_step


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run aviation ETL demo pipeline")
	parser.add_argument(
		"--step",
		choices=["all", "extract", "transform", "load"],
		default="all",
		help="Run full pipeline or a single ETL stage.",
	)
	parser.add_argument(
		"--engine",
		choices=["pandas", "spark"],
		help="Select implementation to run. If omitted, ETL_ENGINE from env is used.",
	)
	parser.add_argument(
		"--input-raw",
		help="Raw JSON path for transform step. If omitted, latest file in data/raw is used.",
	)
	parser.add_argument(
		"--input-valid-csv",
		help="Valid CSV path for load step. If omitted, latest file in data/staging is used.",
	)
	args = parser.parse_args()

	if args.step == "extract":
		print(run_extract_step())
	elif args.step == "transform":
		print(run_transform_step(engine=args.engine, raw_path=args.input_raw))
	elif args.step == "load":
		print(run_load_step(valid_csv_path=args.input_valid_csv))
	else:
		print(run_pipeline(engine=args.engine))
