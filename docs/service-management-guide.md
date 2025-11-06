# Service Management Guide

This guide explains how to use the `manage.sh` script to control all services in the Job Portal application.

## Overview

The `manage.sh` script provides a unified interface to manage:
- **MongoDB** (Docker container)
- **Backend** (FastAPI server)
- **Frontend** (Next.js development server)

## Quick Start

```bash
# Make script executable (first time only)
chmod +x manage.sh

# Start all services
./manage.sh start

# Check status
./manage.sh --status

# Stop all services
./manage.sh stop
```

## Available Commands

### Start Commands

| Command | Description |
|---------|-------------|
| `./manage.sh start` | Start all services (MongoDB, Backend, Frontend) |
| `./manage.sh --start-backend` | Start backend only (also starts MongoDB if needed) |
| `./manage.sh --start-frontend` | Start frontend only |

### Stop Commands

| Command | Description |
|---------|-------------|
| `./manage.sh stop` | Stop all services |
| `./manage.sh --stop-backend` | Stop backend only |
| `./manage.sh --stop-frontend` | Stop frontend only |

### Restart Commands

| Command | Description |
|---------|-------------|
| `./manage.sh restart` | Restart all services (auto-cleans ports) |
| `./manage.sh --restart-backend` | Restart backend only (auto-cleans port 8000) |
| `./manage.sh --restart-frontend` | Restart frontend only (auto-cleans ports 3000/3001) |

**Note:** Restart commands automatically clean up orphaned processes on the required ports before starting services. This ensures a clean restart even if processes were started manually or are out of sync.

### Status Commands

| Command | Description |
|---------|-------------|
| `./manage.sh --status` | Show status of all services |
| `./manage.sh --help` | Show help message with all commands |

## Common Workflows

### Development Workflow

```bash
# Start everything in the morning
./manage.sh start

# Make changes to backend code...
# Backend will auto-reload with uvicorn --reload

# If you need to restart backend manually:
./manage.sh --restart-backend

# Make changes to frontend code...
# Frontend will auto-reload with Next.js

# If you need to restart frontend manually:
./manage.sh --restart-frontend

# Check if everything is running
./manage.sh --status

# End of day - stop everything
./manage.sh stop
```

### Working on Backend Only

```bash
# Start just the backend (and MongoDB)
./manage.sh --start-backend

# Make your changes...

# Restart when needed
./manage.sh --restart-backend

# Stop when done
./manage.sh --stop-backend
```

### Working on Frontend Only

```bash
# Start frontend (assumes backend is already running or not needed)
./manage.sh --start-frontend

# Make your changes...

# Restart when needed
./manage.sh --restart-frontend

# Stop when done
./manage.sh --stop-frontend
```

### Troubleshooting

```bash
# Check what's running
./manage.sh --status

# If services are stuck, restart everything
./manage.sh restart

# View logs if something isn't working
tail -f backend/app.log     # Backend logs
tail -f frontend/app.log    # Frontend logs
```

## Service Details

### MongoDB
- **Port:** 27017
- **Container Name:** job-portal-mongo
- **Management:** Docker container
- **Auto-start:** Automatically started when backend starts

### Backend (FastAPI)
- **Port:** 8000
- **API Docs:** http://localhost:8000/docs
- **Log File:** `backend/app.log`
- **PID File:** `.backend.pid`
- **Auto-reload:** Enabled (via uvicorn --reload)

### Frontend (Next.js)
- **Port:** 3000
- **URL:** http://localhost:3000
- **Log File:** `frontend/app.log`
- **PID File:** `.frontend.pid`
- **Auto-reload:** Enabled (via Next.js dev mode)

## Process Management

The script uses PID files to track running processes:
- `.backend.pid` - Backend process ID
- `.frontend.pid` - Frontend process ID

These files are automatically created when services start and removed when they stop.

## Log Files

All service output is captured in log files:
- `backend/app.log` - Backend API logs
- `frontend/app.log` - Frontend development server logs

To monitor logs in real-time:
```bash
# Backend logs
tail -f backend/app.log

# Frontend logs
tail -f frontend/app.log

# Both logs simultaneously
tail -f backend/app.log frontend/app.log
```

## Error Handling

### "Docker is not running"
**Solution:** Start Docker Desktop before running the script.

### "Port already in use"
**Symptoms:** Service fails to start
**Solution:** 
```bash
# Check what's using the port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Kill the process if needed
kill -9 <PID>

# Or restart the service
./manage.sh --restart-backend
./manage.sh --restart-frontend
```

### "Backend/Frontend failed to start"
**Solution:** Check the log files for detailed error messages:
```bash
cat backend/app.log
cat frontend/app.log
```

### Stale PID Files
If services show as "STOPPED (stale PID file)", the script will automatically clean them up. You can safely start the service again.

## Dependencies

The script automatically handles dependencies:

### Backend Dependencies
- Checks for Python virtual environment
- Creates venv if missing
- Installs requirements.txt automatically

### Frontend Dependencies
- Checks for node_modules
- Runs npm install if missing

## Migration from Old start.sh

The old `start.sh` script has been deprecated and now redirects to `manage.sh start`.

### What Changed?
- ✅ Services now run in background (no need for multiple terminals)
- ✅ Proper process management with PID files
- ✅ Individual service control (restart just backend or frontend)
- ✅ Better error handling and logging
- ✅ Status checking
- ✅ Automatic dependency installation

### Updating Your Workflow
Old command → New command:
```bash
# Old way
./start.sh
# Then manually start backend and frontend in separate terminals

# New way
./manage.sh start
# Everything starts automatically
```

## Best Practices

1. **Always check status first**
   ```bash
   ./manage.sh --status
   ```

2. **Use specific restarts during development**
   ```bash
   # Only restart what you changed
   ./manage.sh --restart-backend
   ```

3. **Monitor logs when debugging**
   ```bash
   tail -f backend/app.log
   ```

4. **Clean shutdown at end of day**
   ```bash
   ./manage.sh stop
   ```

5. **Keep services running during breaks**
   - Services run in background
   - No need to stop/start unless needed
   - Check status when you return

## Advanced Usage

### Running Services on Different Ports

Edit the script to change default ports:
- Backend: Line with `--port 8000`
- Frontend: Line with `npm run dev` (configure in `frontend/package.json`)

### Custom Log Locations

Edit these variables at the top of `manage.sh`:
```bash
BACKEND_LOG_FILE="backend/app.log"
FRONTEND_LOG_FILE="frontend/app.log"
```

### Integration with CI/CD

The script can be used in CI/CD pipelines:
```bash
# In your CI script
./manage.sh start
# Run tests...
./manage.sh stop
```

## Common Issues

### Port Already in Use

**Symptoms:** Service fails to start with message "Port already in use"

**Cause:** Old processes from manual starts are still running and blocking the ports.

**Solution Option 1 (Recommended):**
```bash
# Use restart instead of start - it auto-cleans ports!
./manage.sh restart

# Or restart individual services:
./manage.sh --restart-backend
./manage.sh --restart-frontend
```

**Solution Option 2 (Alternative):**
```bash
# Stop everything first
./manage.sh stop

# Then start fresh
./manage.sh start
```

**Manual cleanup (alternative):**
```bash
# Find and kill process using port 3000 (frontend)
lsof -ti :3000 | xargs kill -9

# Find and kill process using port 8000 (backend)
lsof -ti :8000 | xargs kill -9

# Clean up PID files
rm -f .backend.pid .frontend.pid

# Start services
./manage.sh start
```

### Services Show as "Stopped" But Are Actually Running

**Symptoms:** `./manage.sh --status` shows services as stopped, but ports are in use

**Cause:** Services were started manually (not via manage.sh) or PID files are out of sync

**Solution:**
```bash
# Use restart to reset everything (auto-cleans ports)
./manage.sh restart

# Or stop then start
./manage.sh stop
./manage.sh start
```

### Frontend Running on Port 3001 Instead of 3000

**Symptoms:** 404 error when accessing http://localhost:3000

**Cause:** Port 3000 was already in use, so Next.js automatically used 3001

**Solution:**
```bash
# Use restart to clean up and start fresh
./manage.sh restart

# Frontend will now be on port 3000
```

## Troubleshooting Checklist

- [ ] Is Docker running?
- [ ] Are ports 3000 and 8000 available?
- [ ] Do you have Python 3.11+ installed?
- [ ] Do you have Node.js 18+ installed?
- [ ] Have you tried `./manage.sh restart` to clear orphaned processes?
- [ ] Have you checked the log files?
- [ ] Have you tried restarting the specific service?
- [ ] Have you tried restarting everything?

## Support

For issues or questions:
1. Check the log files first
2. Run `./manage.sh --status` to see service states
3. Refer to the main [README.md](../README.md)
4. Check the [Quick Start Guide](quick-start.md)

## BMAD Methodology Alignment

This service management script follows BMAD (Better Methods for Agile Development) principles:
- **Systematic Approach:** Structured command interface
- **Clear Documentation:** Comprehensive guide with examples
- **Error Handling:** Proper logging and status reporting
- **Maintainability:** Single source of truth for service management
- **Developer Experience:** Simplified workflows for common tasks

