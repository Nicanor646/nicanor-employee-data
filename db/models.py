import os

from sqlalchemy import create_engine

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship



class Base(DeclarativeBase):
    pass

class Deparment(Base):
    __tablename__ = "deparment"

    id:Mapped[int]  = mapped_column( primary_key=True)
    deparment:Mapped[str] = mapped_column(String(100), nullable=False)

    employees: Mapped[List["Employee"]] = relationship(back_populates="deparment")
    
    def __init__(self, name):
        self.deparment = name

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

    deparment:Mapped[Deparment] = relationship(back_populates="employees")
    department_id:Mapped[int] = mapped_column(ForeignKey("deparment.id"))

    job:Mapped[Job] = relationship(back_populates="employees")
    job_id:Mapped[int] = mapped_column(ForeignKey("job.id"))

    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
    DB_NAME = os.environ.get("EMPLOYEE_DB_NAME")
    DB_USER = os.environ.get("EMPLOYEE_DB_USER")
    DB_PASSWORD = os.environ.get("EMPLOYEE_DB_PASSWORD")
    DB_HOST = os.environ.get("EMPLOYEE_DB_HOST", "localhost")
    SQLALCHEMY_DATABASE_URI=f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Base.metadata.create_all(engine)