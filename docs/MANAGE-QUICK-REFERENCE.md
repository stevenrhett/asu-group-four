# manage.sh Quick Reference Card

## Quick Commands

```bash
# Start all services
./manage.sh start

# Stop all services
./manage.sh stop

# Restart all services (auto-cleans ports!)
./manage.sh restart

# Check status
./manage.sh --status

# Get help
./manage.sh --help
```

**✨ NEW:** Restart commands now automatically clean up orphaned processes!

## Service-Specific Commands

```bash
# Backend only
./manage.sh --start-backend
./manage.sh --stop-backend
./manage.sh --restart-backend

# Frontend only
./manage.sh --start-frontend
./manage.sh --stop-frontend
./manage.sh --restart-frontend
```

## Service Endpoints

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/docs |
| MongoDB | 27017 | mongodb://localhost:27017 |

## Log Files

```bash
# View backend logs
tail -f backend/app.log

# View frontend logs
tail -f frontend/app.log

# View both
tail -f backend/app.log frontend/app.log
```

## Common Workflows

### Morning Startup
```bash
./manage.sh start
./manage.sh --status
```

### Quick Backend Restart
```bash
./manage.sh --restart-backend
```

### End of Day
```bash
./manage.sh stop
```

### Troubleshooting

```bash
# Check service status
./manage.sh --status

# View logs
tail -f backend/app.log

# Restart with automatic cleanup (if ports are blocked)
./manage.sh restart
```

## Port Conflicts

If you get "Port already in use" errors:

```bash
./manage.sh restart      # Auto-cleans ports and restarts
```

## Features

✅ Background process management with PID tracking  
✅ Automatic dependency installation  
✅ Color-coded status messages  
✅ Comprehensive error handling  
✅ Individual service control  
✅ Log file capture  
✅ Docker integration for MongoDB  

## Documentation

- Full Guide: [docs/service-management-guide.md](docs/service-management-guide.md)
- Quick Start: [docs/quick-start.md](docs/quick-start.md)
- Main README: [README.md](README.md)

