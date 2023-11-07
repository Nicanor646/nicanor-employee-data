import os
import pandas as pd

from db.models import Department, Job, Employee
from db.db_session_manager import DbSessionManager

CHUNK_SIZE = int(os.environ.get("EMPLOYEE_API_CHUNK_SIZE", 1000))

class CSVETL():
    def __init__(self, csv_file, data_type ) -> None:
        self.csv_file = csv_file
        match data_type:
            case "employee":
                self.DataType = Employee
            case "job":
                self.DataType = Job
            case "department":
                self.DataType = Department
            case _:
                self.DataType = None

    def etl(self):
        # Initialize a chunk reader
        print(self.DataType.get_column_types())
        chunk_reader = pd.read_csv(self.csv_file,
                                   names=self.DataType.get_columns(), 
                                   dtype=self.DataType.get_column_types(),
                                   parse_dates=self.DataType.get_date_columns(),
                                   chunksize=CHUNK_SIZE)
        with DbSessionManager(self.DataType) as db_session:
            for chunk in chunk_reader:
                # Dropping rows with missing values
                chunk_row_list = chunk.dropna().to_dict(orient='records')
                # TODO: Check data quality here
                db_session.insert_data(chunk_row_list)

            