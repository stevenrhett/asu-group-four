# Troubleshooting: 404 Error After Using manage.sh

## What Happened

After implementing the new `manage.sh` script, you encountered a 404 error. The investigation revealed:

### Root Cause
You had **multiple instances** of services running simultaneously:
- **Port 3000**: Old Node.js process (PID 56885) from manual start
- **Port 8000**: Multiple Python/uvicorn processes (both old and new)

When the new `manage.sh` tried to start services:
- Backend couldn't bind to port 8000 (already in use by old processes)
- Frontend couldn't bind to port 3000, so Next.js automatically used port 3001
- You accessed `http://localhost:3000` but frontend was on `http://localhost:3001` → **404 Error**

### Why This Happened
Before `manage.sh` was created, you were starting services manually in separate terminals. These processes kept running in the background even after the `manage.sh` script was introduced, causing port conflicts.

## Solution

### Step 1: Restart Services with Automatic Cleanup

Use the restart command which automatically cleans up all orphaned processes:

```bash
./manage.sh restart
```

This will:
- Kill all processes on ports 3000 and 3001 (frontend)
- Kill all processes on port 8000 (backend)
- Remove stale PID files
- Start all services fresh

### Step 2: Verify Status

Start all services properly with the management script:

```bash
./manage.sh start
```

### Step 3: Verify Everything is Running

```bash
./manage.sh --status
```

You should see:
```
✅ MongoDB: RUNNING (port 27017)
✅ Backend: RUNNING (PID: XXXX, Port: 8000)
✅ Frontend: RUNNING (PID: XXXX, Port: 3000)
```

### Step 4: Access the Application

Now you can access:
- **Frontend**: http://localhost:3000 ✅
- **Backend API**: http://localhost:8000 ✅
- **API Docs**: http://localhost:8000/docs ✅

## Prevention

To avoid this issue in the future:

### ✅ DO:
- **Always use `./manage.sh`** to start/stop services
- Run `./manage.sh --status` to check what's running
- Use `./manage.sh restart` to handle any port conflicts automatically
- Use `./manage.sh restart` instead of stopping and starting manually

### ❌ DON'T:
- Start services manually in separate terminals (old method)
- Use `uvicorn` or `npm run dev` directly
- Mix manual starts with `manage.sh` starts
- Leave services running when switching between management methods

## Improved manage.sh Features

The script has been enhanced to detect and prevent this issue:

### Port Conflict Detection & Automatic Cleanup
```bash
# Restart automatically cleans ports
./manage.sh restart

# If starting and port is blocked, you'll see:
❌ Port 8000 is already in use (PID: 12345)
ℹ️  Use './manage.sh restart' to automatically clean up
ℹ️  Or manually kill: kill -9 12345
```

### Better Status Reporting
```bash
./manage.sh --status
```
Shows actual port usage and PID information for all services.

### Automatic Cleanup on Restart
```bash
# Restart command handles everything
./manage.sh restart

# Automatically:
# - Kills orphaned processes
# - Cleans up ports
# - Removes stale PID files
# - Starts services fresh
```

## Manual Cleanup (Alternative)

If you prefer to clean up manually instead of using the cleanup script:

```bash
# Kill frontend (port 3000)
lsof -ti :3000 | xargs kill -9

# Kill backend (port 8000)
lsof -ti :8000 | xargs kill -9

# Remove PID files
rm -f .backend.pid .frontend.pid

# Start fresh
./manage.sh start
```

## Checking What's Running

### Check specific ports:
```bash
# What's on port 3000?
lsof -i :3000

# What's on port 8000?
lsof -i :8000

# What's on port 27017? (MongoDB)
lsof -i :27017
```

### Check all Node/Python processes:
```bash
# All Node processes
ps aux | grep node | grep -v grep

# All Python/uvicorn processes
ps aux | grep uvicorn | grep -v grep
```

## Log Files

If you need to debug what went wrong, check the logs:

```bash
# Backend logs
tail -50 backend/app.log

# Frontend logs
tail -50 frontend/app.log

# Follow logs in real-time
tail -f backend/app.log frontend/app.log
```

## Quick Reference

```bash
# 1. Restart with automatic cleanup
./manage.sh restart

# 2. Verify status
./manage.sh --status

# 3. Access frontend
open http://localhost:3000

# 4. If issues persist, check logs
tail -f backend/app.log
```

## Summary

**Problem:** Port conflicts from manual starts caused 404 errors  
**Solution:** Use `cleanup-services.sh` to reset, then always use `manage.sh`  
**Prevention:** Never mix manual starts with `manage.sh` management  

---

## Enhancements Made to Fix This

1. **Improved `manage.sh`** - Now includes automatic port cleanup on restart
2. **Port conflict detection** - Detects conflicts before starting
3. **Updated documentation** - Added troubleshooting sections

## Next Steps

After cleaning up and restarting:
1. Verify all services are on correct ports
2. Test frontend access at http://localhost:3000
3. Test backend API at http://localhost:8000/docs
4. From now on, only use `./manage.sh` for service management

---

**Your services should now be working correctly! 🚀**

