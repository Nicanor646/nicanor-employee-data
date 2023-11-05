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
        return [c_attr.key for c_attr in inst.mapper.column_attrs]
        

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
    engine = get_engine()
    Base.metadata.create_all(engine)