from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
import crud
import schemas
from models import TimeEntry, Worker, Project, SubDepartment, ProductionLine

app = FastAPI(title="Plant Time Tracker API", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API Routes

# Department endpoints
@app.post("/api/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db=db, department=department)

@app.get("/api/departments/", response_model=List[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_departments(db, skip=skip, limit=limit)

@app.get("/api/departments/{department_id}", response_model=schemas.Department)
def read_department(department_id: int, db: Session = Depends(get_db)):
    department = crud.get_department(db, department_id=department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

# SubDepartment endpoints
@app.post("/api/sub-departments/", response_model=schemas.SubDepartment)
def create_sub_department(sub_department: schemas.SubDepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_sub_department(db=db, sub_department=sub_department)

@app.get("/api/sub-departments/", response_model=List[schemas.SubDepartment])
def read_sub_departments(department_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_sub_departments(db, department_id=department_id)

# ProductionLine endpoints
@app.post("/api/production-lines/", response_model=schemas.ProductionLine)
def create_production_line(production_line: schemas.ProductionLineCreate, db: Session = Depends(get_db)):
    return crud.create_production_line(db=db, production_line=production_line)

@app.get("/api/production-lines/", response_model=List[schemas.ProductionLine])
def read_production_lines(db: Session = Depends(get_db)):
    return crud.get_production_lines(db)

# Worker endpoints
@app.post("/api/workers/", response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    return crud.create_worker(db=db, worker=worker)

@app.get("/api/workers/", response_model=List[schemas.Worker])
def read_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_workers(db, skip=skip, limit=limit)

@app.get("/api/workers/{worker_id}", response_model=schemas.Worker)
def read_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = crud.get_worker(db, worker_id=worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

# Project endpoints
@app.post("/api/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@app.get("/api/projects/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_projects(db, skip=skip, limit=limit)

@app.get("/api/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# TimeEntry endpoints
@app.post("/api/time-entries/", response_model=schemas.TimeEntry)
def create_time_entry(time_entry: schemas.TimeEntryCreate, db: Session = Depends(get_db)):
    return crud.create_time_entry(db=db, time_entry=time_entry)

@app.get("/api/time-entries/", response_model=List[schemas.TimeEntry])
def read_time_entries(skip: int = 0, limit: int = 100, worker_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_time_entries(db, skip=skip, limit=limit, worker_id=worker_id)

@app.get("/api/time-entries/{time_entry_id}", response_model=schemas.TimeEntry)
def read_time_entry(time_entry_id: int, db: Session = Depends(get_db)):
    time_entry = crud.get_time_entry(db, time_entry_id=time_entry_id)
    if time_entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return time_entry

@app.put("/api/time-entries/{time_entry_id}", response_model=schemas.TimeEntry)
def update_time_entry(time_entry_id: int, time_entry_update: schemas.TimeEntryUpdate, db: Session = Depends(get_db)):
    time_entry = crud.update_time_entry(db, time_entry_id=time_entry_id, time_entry_update=time_entry_update)
    if time_entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return time_entry

@app.get("/api/time-entries/active/", response_model=List[schemas.TimeEntry])
def read_active_time_entries(worker_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_active_time_entries(db, worker_id=worker_id)

# Clock in/out endpoints
@app.post("/api/clock-in/")
def clock_in(worker_id: int = Form(...), project_id: int = Form(...), sub_department_id: int = Form(...), production_line_id: int = Form(...), 
            description: Optional[str] = Form(None), db: Session = Depends(get_db)):
    # Check if worker already has an active time entry
    active_entries = crud.get_active_time_entries(db, worker_id=worker_id)
    if active_entries:
        raise HTTPException(status_code=400, detail="Worker already has an active time entry")
    
    time_entry = schemas.TimeEntryCreate(
        worker_id=worker_id,
        project_id=project_id,
        sub_department_id=sub_department_id,
        production_line_id=production_line_id,
        start_time=datetime.now(),
        description=description
    )
    return crud.create_time_entry(db=db, time_entry=time_entry)

@app.post("/api/clock-out/{time_entry_id}")
def clock_out(time_entry_id: int, db: Session = Depends(get_db)):
    time_entry_update = schemas.TimeEntryUpdate(end_time=datetime.now())
    time_entry = crud.update_time_entry(db, time_entry_id=time_entry_id, time_entry_update=time_entry_update)
    if time_entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return time_entry

# Web UI Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    workers = crud.get_workers(db)
    projects = crud.get_projects(db)
    departments = crud.get_departments(db)
    production_lines = crud.get_production_lines(db)
    active_entries = crud.get_active_time_entries(db)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "workers": workers,
        "projects": projects,
        "departments": departments,
        "production_lines": production_lines,
        "active_entries": active_entries
    })

@app.get("/setup", response_class=HTMLResponse)
async def setup(request: Request, db: Session = Depends(get_db)):
    departments = crud.get_departments(db)
    sub_departments = crud.get_sub_departments(db)
    production_lines = crud.get_production_lines(db)
    workers = crud.get_workers(db)
    projects = crud.get_projects(db)
    
    return templates.TemplateResponse("setup.html", {
        "request": request,
        "departments": departments,
        "sub_departments": sub_departments,
        "production_lines": production_lines,
        "workers": workers,
        "projects": projects
    })

@app.get("/reports", response_class=HTMLResponse)
async def reports(request: Request, db: Session = Depends(get_db)):
    time_entries = crud.get_time_entries(db, limit=50)
    workers = crud.get_workers(db)
    projects = crud.get_projects(db)
    
    # Convert time entries to serializable format
    time_entries_data = []
    for entry in time_entries:
        entry_dict = {
            "id": entry.id,
            "worker_id": entry.worker_id,
            "project_id": entry.project_id,
            "sub_department_id": entry.sub_department_id,
            "production_line_id": entry.production_line_id,
            "start_time": entry.start_time.isoformat() if entry.start_time else None,
            "end_time": entry.end_time.isoformat() if entry.end_time else None,
            "hours_worked": entry.hours_worked,
            "description": entry.description,
            "created_at": entry.created_at.isoformat() if entry.created_at else None,
            "worker": {
                "id": entry.worker.id,
                "name": entry.worker.name,
                "employee_id": entry.worker.employee_id
            },
            "project": {
                "id": entry.project.id,
                "name": entry.project.name,
                "description": entry.project.description
            },
            "sub_department": {
                "id": entry.sub_department.id,
                "name": entry.sub_department.name,
                "department_id": entry.sub_department.department_id,
                "department": {
                    "id": entry.sub_department.department.id,
                    "name": entry.sub_department.department.name,
                    "description": entry.sub_department.department.description
                }
            },
            "production_line": {
                "id": entry.production_line.id,
                "name": entry.production_line.name,
                "description": entry.production_line.description
            }
        }
        time_entries_data.append(entry_dict)
    
    return templates.TemplateResponse("reports.html", {
        "request": request,
        "time_entries": time_entries,  # Keep original for template rendering
        "time_entries_data": time_entries_data,  # Serializable data for JavaScript
        "workers": workers,
        "projects": projects
    })

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(app, host="0.0.0.0", port=port)

