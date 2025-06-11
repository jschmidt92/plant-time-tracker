# Docker Setup Instructions

## Quick Start

1. **Clone or download the application**
2. **Create a .env file** (optional, for custom configuration)
3. **Build and run with Docker Compose**

## Environment Configuration

### Using a .env file

To customize the application settings, create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Then edit the `.env` file:

```bash
# Port configuration
PORT=9002
```

### Available Environment Variables

- `PORT`: The port the application will run on (default: 8000)

## Running with Docker Compose

### With default settings (port 8000):
```bash
docker-compose up -d --build
```

### With custom port via .env file:
1. Create `.env` file with `PORT=9002`
2. Run:
```bash
docker-compose up -d --build
```

### With custom port via command line:
```bash
PORT=9002 docker-compose up -d --build
```

## How the Port Configuration Works

1. **main.py**: Reads the `PORT` environment variable, defaults to 8000
2. **docker-compose.yml**: Uses `${PORT:-8000}` to read from .env or default to 8000
3. **Dockerfile**: Sets `ENV PORT=8000` as container default

## Accessing the Application

- If using default port: http://localhost:8000
- If using custom port (e.g., 9002): http://localhost:9002

## Stopping the Application

```bash
docker-compose down
```

## Viewing Logs

```bash
docker-compose logs -f plant-time-tracker
```

## Database Persistence

The SQLite database is mounted as a volume, so your data will persist between container restarts:
- Local file: `./plant_time_tracker.db`
- Container path: `/app/plant_time_tracker.db`

## Security Notes

- The `.env` file is excluded from the Docker image for security
- Never commit `.env` files to version control
- Use `.env.example` as a template for required variables

