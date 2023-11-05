import os

from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy.orm import Session


def get_engine():
    DB_NAME = os.environ.get("EMPLOYEE_DB_NAME")
    DB_USER = os.environ.get("EMPLOYEE_DB_USER")
    DB_PASSWORD = os.environ.get("EMPLOYEE_DB_PASSWORD")
    DB_HOST = os.environ.get("EMPLOYEE_DB_HOST", "localhost")
    SQLALCHEMY_DATABASE_URI=f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    return engine

class DbSessionManager():
    def __init__(self, DataType) -> None:
        self.DataType = DataType
        
    def __enter__(self):
        self.engine = get_engine()
        self.db_session = Session(self.engine)
        return self

    def __exit__(self, excep_type, excep_value, excep_traceback):
        self.db_session.commit()
        self.db_session.close()
        print(f"The process had a {excep_type} with value {excep_value}")
        # print(excep_traceback)
        return True

    def insert_data(self, data, commit=False):
        self.db_session.execute(
            insert(self.DataType),
            data
        )
        if commit:
            self.db_session.commit()
        return 0
