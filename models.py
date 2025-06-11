from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(255))
    
    sub_departments = relationship("SubDepartment", back_populates="department")

class SubDepartment(Base):
    __tablename__ = "sub_departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    department = relationship("Department", back_populates="sub_departments")
    time_entries = relationship("TimeEntry", back_populates="sub_department")

class ProductionLine(Base):
    __tablename__ = "production_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(255))
    
    time_entries = relationship("TimeEntry", back_populates="production_line")

class Worker(Base):
    __tablename__ = "workers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    employee_id = Column(String(50), unique=True, index=True)
    
    time_entries = relationship("TimeEntry", back_populates="worker")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    time_entries = relationship("TimeEntry", back_populates="project")

class TimeEntry(Base):
    __tablename__ = "time_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    sub_department_id = Column(Integer, ForeignKey("sub_departments.id"))
    production_line_id = Column(Integer, ForeignKey("production_lines.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    hours_worked = Column(Float, nullable=True)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    worker = relationship("Worker", back_populates="time_entries")
    project = relationship("Project", back_populates="time_entries")
    sub_department = relationship("SubDepartment", back_populates="time_entries")
    production_line = relationship("ProductionLine", back_populates="time_entries")

