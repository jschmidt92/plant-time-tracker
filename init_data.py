#!/usr/bin/env python3
"""
Initialization script to set up sample data for the Plant Time Tracker.
This creates the Wall department with sub-departments, production lines,
some sample workers and projects.
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Department, SubDepartment, ProductionLine, Worker, Project

def init_database():
    """Initialize the database with sample data"""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Department).first():
            print("Database already contains data. Skipping initialization.")
            return
        
        # Create Wall Department
        wall_dept = Department(
            name="Wall",
            description="Wall manufacturing department"
        )
        db.add(wall_dept)
        db.commit()
        db.refresh(wall_dept)
        
        # Create Sub-departments
        sub_departments = [
            SubDepartment(name="Cutting", department_id=wall_dept.id),
            SubDepartment(name="Framing", department_id=wall_dept.id),
            SubDepartment(name="Sheeting/Typar", department_id=wall_dept.id),
            SubDepartment(name="Window/Door Installation", department_id=wall_dept.id),
            SubDepartment(name="Loading", department_id=wall_dept.id),
        ]
        
        for sub_dept in sub_departments:
            db.add(sub_dept)
        
        # Create Production Lines
        production_lines = [
            ProductionLine(name="Line 1", description="Primary production line"),
            ProductionLine(name="Line 2", description="Secondary production line"),
            ProductionLine(name="Line 3", description="Tertiary production line"),
        ]
        
        for line in production_lines:
            db.add(line)
        
        # Create Sample Workers
        workers = [
            Worker(name="John Smith", employee_id="EMP001"),
            Worker(name="Sarah Johnson", employee_id="EMP002"),
            Worker(name="Mike Wilson", employee_id="EMP003"),
            Worker(name="Emily Davis", employee_id="EMP004"),
            Worker(name="David Brown", employee_id="EMP005"),
        ]
        
        for worker in workers:
            db.add(worker)
        
        # Create Sample Projects
        projects = [
            Project(name="Residential Complex A", description="200-unit residential project"),
            Project(name="Commercial Building B", description="Office building construction"),
            Project(name="School Renovation", description="Elementary school wall renovation"),
            Project(name="Hospital Extension", description="Hospital wing addition"),
        ]
        
        for project in projects:
            db.add(project)
        
        db.commit()
        
        print("✅ Database initialized successfully!")
        print(f"Created:")
        print(f"  - 1 Department (Wall)")
        print(f"  - {len(sub_departments)} Sub-departments")
        print(f"  - {len(production_lines)} Production lines")
        print(f"  - {len(workers)} Workers")
        print(f"  - {len(projects)} Projects")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing Plant Time Tracker database...")
    init_database()
    print("\nYou can now start the application with: python main.py")

