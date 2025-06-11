from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Department Schemas
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    
    class Config:
        from_attributes = True

# SubDepartment Schemas
class SubDepartmentBase(BaseModel):
    name: str
    department_id: int

class SubDepartmentCreate(SubDepartmentBase):
    pass

class SubDepartment(SubDepartmentBase):
    id: int
    
    class Config:
        from_attributes = True

# ProductionLine Schemas
class ProductionLineBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProductionLineCreate(ProductionLineBase):
    pass

class ProductionLine(ProductionLineBase):
    id: int
    
    class Config:
        from_attributes = True

# Worker Schemas
class WorkerBase(BaseModel):
    name: str
    employee_id: str

class WorkerCreate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int
    
    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# TimeEntry Schemas
class TimeEntryBase(BaseModel):
    worker_id: int
    project_id: int
    sub_department_id: int
    production_line_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    hours_worked: Optional[float] = None
    description: Optional[str] = None

class TimeEntryCreate(TimeEntryBase):
    pass

class TimeEntryUpdate(BaseModel):
    end_time: Optional[datetime] = None
    hours_worked: Optional[float] = None
    description: Optional[str] = None

class TimeEntry(TimeEntryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Response schemas with relationships
class DepartmentWithSubs(Department):
    sub_departments: List[SubDepartment] = []

class TimeEntryWithDetails(TimeEntry):
    worker: Worker
    project: Project
    sub_department: SubDepartment
    production_line: ProductionLine

