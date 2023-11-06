import os

from typing import List
from typing import Optional
from sqlalchemy import inspect
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    @classmethod
    def get_columns(cls):
        inst = inspect(cls)
        columns = inst.c
        return columns.keys()
    
    @classmethod
    def get_column_types(cls):
        inst = inspect(cls)
        columns = inst.c
        column_names = columns.keys()
        column_types={}
        for column in column_names:
            python_type = str(columns[column].type.python_type).split("'")[1]
            if 'datetime' in python_type:
                column_types[column] = 'str'
            elif python_type == 'int':
                column_types[column] = 'Int64'
            else:
                column_types[column] = python_type
        return column_types

    @classmethod
    def get_date_columns(cls):
        inst = inspect(cls)
        columns = inst.c
        column_names = columns.keys()
        date_columns=[]
        for column in column_names:
            python_type = str(columns[column].type.python_type).split("'")[1]
            if 'datetime' in python_type:
                date_columns.append(column)
        return date_columns
        

class Department(Base):
    __tablename__ = "department"

    id:Mapped[int]  = mapped_column( primary_key=True)
    department:Mapped[str] = mapped_column(String(100), nullable=False)

    employees: Mapped[List["Employee"]] = relationship(back_populates="department")
    
    def __init__(self, name):
        self.department = name

class Job(Base):
    __tablename__ = "job"

    id:Mapped[int]  = mapped_column(Integer, primary_key=True)
    job:Mapped[str] = mapped_column(String(100), nullable=False)

    employees: Mapped[List["Employee"]] = relationship(back_populates="job")
    
    def __init__(self, name):
        self.job = name

class Employee(Base):
    __tablename__ = "employee"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(120), nullable=False)
    datetime:Mapped[datetime] = mapped_column(DateTime())

    department:Mapped[Department] = relationship(back_populates="employees")
    department_id:Mapped[int] = mapped_column(ForeignKey("department.id"))

    job:Mapped[Job] = relationship(back_populates="employees")
    job_id:Mapped[int] = mapped_column(ForeignKey("job.id"))

    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
    from db_session_manager import get_engine
    engine = get_engine()
    Base.metadata.create_all(engine)