from sqlalchemy.orm import Session
from models import Department, SubDepartment, ProductionLine, Worker, Project, TimeEntry
from schemas import (
    DepartmentCreate, SubDepartmentCreate, ProductionLineCreate, 
    WorkerCreate, ProjectCreate, TimeEntryCreate, TimeEntryUpdate
)
from datetime import datetime
from typing import List, Optional

# Department CRUD
def create_department(db: Session, department: DepartmentCreate):
    # Check if department already exists
    existing_dept = db.query(Department).filter(Department.name == department.name).first()
    if existing_dept:
        return existing_dept
    
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Department).offset(skip).limit(limit).all()

def get_department(db: Session, department_id: int):
    return db.query(Department).filter(Department.id == department_id).first()

# SubDepartment CRUD
def create_sub_department(db: Session, sub_department: SubDepartmentCreate):
    # Check if sub-department already exists with the same name and department
    existing_sub_dept = db.query(SubDepartment).filter(
        SubDepartment.name == sub_department.name,
        SubDepartment.department_id == sub_department.department_id
    ).first()
    if existing_sub_dept:
        return existing_sub_dept
    
    db_sub_department = SubDepartment(**sub_department.dict())
    db.add(db_sub_department)
    db.commit()
    db.refresh(db_sub_department)
    return db_sub_department

def get_sub_departments(db: Session, department_id: Optional[int] = None):
    query = db.query(SubDepartment)
    if department_id:
        query = query.filter(SubDepartment.department_id == department_id)
    return query.all()

# ProductionLine CRUD
def create_production_line(db: Session, production_line: ProductionLineCreate):
    # Check if production line already exists
    existing_line = db.query(ProductionLine).filter(ProductionLine.name == production_line.name).first()
    if existing_line:
        return existing_line
    
    db_production_line = ProductionLine(**production_line.dict())
    db.add(db_production_line)
    db.commit()
    db.refresh(db_production_line)
    return db_production_line

def get_production_lines(db: Session):
    return db.query(ProductionLine).all()

# Worker CRUD
def create_worker(db: Session, worker: WorkerCreate):
    # Check if worker already exists with the same employee_id
    existing_worker = db.query(Worker).filter(Worker.employee_id == worker.employee_id).first()
    if existing_worker:
        return existing_worker
    
    db_worker = Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def get_workers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Worker).offset(skip).limit(limit).all()

def get_worker(db: Session, worker_id: int):
    return db.query(Worker).filter(Worker.id == worker_id).first()

# Project CRUD
def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

# TimeEntry CRUD
def create_time_entry(db: Session, time_entry: TimeEntryCreate):
    db_time_entry = TimeEntry(**time_entry.dict())
    db.add(db_time_entry)
    db.commit()
    db.refresh(db_time_entry)
    return db_time_entry

def get_time_entries(db: Session, skip: int = 0, limit: int = 100, worker_id: Optional[int] = None):
    query = db.query(TimeEntry)
    if worker_id:
        query = query.filter(TimeEntry.worker_id == worker_id)
    return query.offset(skip).limit(limit).all()

def get_time_entry(db: Session, time_entry_id: int):
    return db.query(TimeEntry).filter(TimeEntry.id == time_entry_id).first()

def update_time_entry(db: Session, time_entry_id: int, time_entry_update: TimeEntryUpdate):
    db_time_entry = db.query(TimeEntry).filter(TimeEntry.id == time_entry_id).first()
    if db_time_entry:
        update_data = time_entry_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_time_entry, field, value)
        
        # Calculate hours if both start and end time are available
        if db_time_entry.start_time and db_time_entry.end_time:
            duration = db_time_entry.end_time - db_time_entry.start_time
            db_time_entry.hours_worked = duration.total_seconds() / 3600
        
        db.commit()
        db.refresh(db_time_entry)
    return db_time_entry

def get_active_time_entries(db: Session, worker_id: Optional[int] = None):
    """Get time entries that haven't been completed (no end_time)"""
    query = db.query(TimeEntry).filter(TimeEntry.end_time.is_(None))
    if worker_id:
        query = query.filter(TimeEntry.worker_id == worker_id)
    return query.all()

