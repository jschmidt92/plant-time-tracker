# Plant Time Tracker

A web-based time tracking system designed for manufacturing plants to track worker time across different departments, sub-departments, and production lines.

## Features

- **Department Management**: Organize work by departments and sub-departments
- **Production Line Tracking**: Track time across multiple production lines
- **Worker Management**: Manage worker profiles and employee IDs
- **Project Tracking**: Associate time entries with specific projects
- **Clock In/Out System**: Simple interface for workers to clock in and out
- **Real-time Dashboard**: See active workers and quick statistics
- **Reporting**: Detailed reports with filtering and export capabilities
- **Charts and Analytics**: Visual representation of time data

## Pre-configured for Wall Department

The system comes pre-configured with a Wall department structure:
- **Department**: Wall
- **Sub-departments**: 
  - Cutting
  - Framing
  - Sheeting/Typar
  - Window/Door Installation
  - Loading
- **Production Lines**: Line 1, Line 2, Line 3

## Installation

1. **Clone or download the project**:
   ```bash
   cd plant-time-tracker
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   ```bash
   python init_data.py
   ```

4. **Start the application**:
   ```bash
   python main.py
   ```

5. **Open your web browser** and navigate to:
   ```
   http://localhost:8000
   ```

## Usage

### Dashboard (Main Page)
- Clock workers in and out
- View currently active workers
- See quick statistics
- Clock out active workers

### Setup Page
- Add new departments, sub-departments, and production lines
- Register new workers
- Create new projects
- Quick setup button for Wall department structure

### Reports Page
- View all time entries in a table format
- Filter by worker, project, or date range
- Export data to CSV
- View charts showing hours by worker and project
- Summary statistics

## API Endpoints

The application provides a RESTful API with the following main endpoints:

### Departments
- `GET /api/departments/` - List all departments
- `POST /api/departments/` - Create a new department
- `GET /api/departments/{id}` - Get specific department

### Sub-Departments
- `GET /api/sub-departments/` - List all sub-departments
- `POST /api/sub-departments/` - Create a new sub-department
- `GET /api/sub-departments/?department_id={id}` - Get sub-departments for a department

### Production Lines
- `GET /api/production-lines/` - List all production lines
- `POST /api/production-lines/` - Create a new production line

### Workers
- `GET /api/workers/` - List all workers
- `POST /api/workers/` - Create a new worker
- `GET /api/workers/{id}` - Get specific worker

### Projects
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create a new project
- `GET /api/projects/{id}` - Get specific project

### Time Entries
- `GET /api/time-entries/` - List all time entries
- `POST /api/time-entries/` - Create a new time entry
- `GET /api/time-entries/{id}` - Get specific time entry
- `PUT /api/time-entries/{id}` - Update time entry
- `GET /api/time-entries/active/` - Get active (not clocked out) entries

### Clock In/Out
- `POST /api/clock-in/` - Clock in a worker
- `POST /api/clock-out/{time_entry_id}` - Clock out a worker

## Database

The application uses SQLite for data storage with the following main tables:
- `departments` - Department information
- `sub_departments` - Sub-department information
- `production_lines` - Production line information
- `workers` - Worker profiles
- `projects` - Project information
- `time_entries` - Time tracking records

## Sample Data

The initialization script creates:
- 1 Wall department with 5 sub-departments
- 3 production lines
- 5 sample workers
- 4 sample projects

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, Bootstrap 5, JavaScript
- **Charts**: Chart.js
- **Icons**: Font Awesome

## Customization

To customize for your plant:

1. **Add your departments**: Use the Setup page or API to add your specific departments
2. **Configure sub-departments**: Add the sub-departments that match your workflow
3. **Set up production lines**: Configure your actual production lines
4. **Register workers**: Add your workers with their employee IDs
5. **Create projects**: Set up your current projects

## Development

To modify or extend the application:

1. **Models**: Edit `models.py` to change database structure
2. **API**: Modify `main.py` to add new endpoints
3. **Frontend**: Edit HTML templates in `templates/` directory
4. **Business Logic**: Update `crud.py` for database operations

## Support

This application is designed to be simple and self-contained. All data is stored locally in SQLite, and the web interface provides full functionality for time tracking in a manufacturing environment.

