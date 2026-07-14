from src.etl.loader import load_all_files
from src.etl.validator import DataValidator

datasets = load_all_files()

validator = DataValidator(datasets)
validator.run_all()