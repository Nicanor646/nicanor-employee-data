import os

from db.db_session_manager import DbSessionManager

SQL_EMPLOYEE_BY_Q= os.environ.get("EMPLOYEE_SQL_EMPLOYEE_BY_Q", "sql/employees_by_q.sql")

class Report():

    def employees_by_q(self,year=2021):
        with DbSessionManager(None) as db_session, \
            open(SQL_EMPLOYEE_BY_Q) as sql_file:
            sql_query = sql_file.read()
            values = {"year": year}
            results = db_session.run_query(sql_query,values)
            return [ r._asdict() for r in results ]