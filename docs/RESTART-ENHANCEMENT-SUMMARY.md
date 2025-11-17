# Restart Enhancement - Automatic Port Cleanup

## Summary

The `manage.sh` script has been enhanced with **automatic port cleanup** in all restart operations. This solves the 404 error issue you experienced and prevents future port conflicts.

## What Changed

### Before (Issue)
```bash
# Old manual process blocking port 3000
./manage.sh start
# ❌ Error: Port 3000 already in use
# Frontend starts on port 3001 instead
# http://localhost:3000 → 404 Error
```

### After (Fixed)
```bash
./manage.sh restart
# ✅ Automatically kills processes on ports 3000, 3001, 8000
# ✅ Clears all PID files
# ✅ Starts fresh on correct ports
# ✅ http://localhost:3000 → Works!
```

## New Features

### 1. Force Cleanup Functions

#### `force_cleanup_backend()`
- Kills all processes on port 8000
- Terminates any uvicorn processes
- Removes stale PID files
- Used automatically on `./manage.sh --restart-backend`

#### `force_cleanup_frontend()`
- Kills all processes on ports 3000 and 3001
- Terminates any Next.js dev processes
- Removes stale PID files
- Used automatically on `./manage.sh --restart-frontend`

#### `cleanup_port(port, service_name)`
- Reusable function to clean any specific port
- Provides clear feedback
- Used by both stop and restart operations

### 2. Enhanced Restart Commands

All restart operations now include automatic cleanup:

```bash
# Restart everything with full cleanup
./manage.sh restart

# Restart backend only (cleans port 8000)
./manage.sh --restart-backend

# Restart frontend only (cleans ports 3000/3001)
./manage.sh --restart-frontend
```

### 3. Improved Stop Commands

Stop operations now check both PID files AND ports:

```bash
./manage.sh stop
# 1. Attempts graceful stop via PID
# 2. Scans and kills any remaining processes on ports
# 3. Ensures complete cleanup
```

## Usage

### Recommended Workflow

```bash
# Daily use - just restart when needed
./manage.sh restart

# Individual service restart
./manage.sh --restart-backend    # After backend changes
./manage.sh --restart-frontend   # After frontend changes

# Check status anytime
./manage.sh --status
```

### Solving Port Conflicts

**Old way (no longer needed):**
```bash
./cleanup-services.sh
./manage.sh start
```

**New way (automatic):**
```bash
./manage.sh restart  # Does it all!
```

## Technical Details

### What Gets Cleaned

#### Backend Restart:
- ✅ All processes on port 8000
- ✅ All uvicorn processes matching `app.main`
- ✅ `.backend.pid` file
- ✅ Ensures MongoDB is running

#### Frontend Restart:
- ✅ All processes on port 3000
- ✅ All processes on port 3001 (fallback port)
- ✅ All Next.js dev server processes
- ✅ `.frontend.pid` file

#### Full Restart:
- ✅ All of the above
- ✅ MongoDB container restart
- ✅ Fresh start for all services

### Execution Flow

```
./manage.sh restart
    ↓
1. Force cleanup frontend
    - Kill port 3000 processes
    - Kill port 3001 processes
    - Kill Next.js processes
    - Remove .frontend.pid
    ↓
2. Force cleanup backend
    - Kill port 8000 processes
    - Kill uvicorn processes
    - Remove .backend.pid
    ↓
3. Restart MongoDB
    - Docker restart if running
    ↓
4. Start MongoDB
    - Ensure container is up
    ↓
5. Start Backend
    - Fresh process on port 8000
    ↓
6. Start Frontend
    - Fresh process on port 3000
    ↓
✅ All services running cleanly!
```

## Benefits

### 1. No More Port Conflicts
- Restart always succeeds
- No manual intervention needed
- Automatic cleanup of orphaned processes

### 2. Faster Development
- Quick restarts during development
- No need to run separate cleanup scripts
- Single command does everything

### 3. Prevents Issues
- Frontend always on port 3000 (not 3001)
- Backend always on port 8000
- No stale PID files
- No zombie processes

### 4. Better Reliability
- Restart is now idempotent
- Works even if services were started manually
- Handles edge cases automatically

## Backward Compatibility

✅ All existing commands work unchanged
✅ No breaking changes
✅ `cleanup-services.sh` still available if needed
✅ Manual start/stop still supported

## When to Use What

### Use `restart` when:
- ✅ Developing and need to reload code
- ✅ You suspect orphaned processes
- ✅ Ports might be blocked
- ✅ Want a guaranteed clean start

### Use `start` when:
- Services are completely stopped
- First time starting
- No port conflicts expected

### Use `stop` when:
- Ending work session
- Need to free resources
- Switching to manual management

### Use `cleanup-services.sh` when:
- Need to clear logs too
- Want interactive cleanup
- Manual verification preferred

## Examples

### Fix Your Current 404 Issue
```bash
cd /Users/davidnwankwo/Documents/Notes/ASU_Revature/asu-group-four
./manage.sh restart
# ✅ Ports cleaned, services started correctly
# ✅ http://localhost:3000 now works!
```

### Development Workflow
```bash
# Morning: Start everything
./manage.sh start

# Make backend changes...
./manage.sh --restart-backend

# Make frontend changes...
./manage.sh --restart-frontend

# Issues? Full restart
./manage.sh restart

# End of day
./manage.sh stop
```

### Troubleshooting
```bash
# Check what's running
./manage.sh --status

# Force restart everything
./manage.sh restart

# Still issues? Check logs
tail -f backend/app.log frontend/app.log
```

## Files Modified

1. **manage.sh**
   - Added `cleanup_port()` function
   - Added `force_cleanup_backend()` function
   - Added `force_cleanup_frontend()` function
   - Enhanced `stop_backend()` to clean ports
   - Enhanced `stop_frontend()` to clean ports
   - Rewrote `restart_all()` with force cleanup
   - Rewrote `restart_backend()` with force cleanup
   - Rewrote `restart_frontend()` with force cleanup

2. **Documentation**
   - Updated docs/service-management-guide.md
   - Updated docs/MANAGE-QUICK-REFERENCE.md
   - Updated README.md
   - Created docs/CHANGELOG.md
   - Created this summary document

## Next Steps for You

### Immediate Action
```bash
# Fix your current 404 issue
./manage.sh restart
```

### Going Forward
```bash
# Always use restart instead of manual cleanup
./manage.sh restart              # Not: cleanup → start
./manage.sh --restart-backend    # Not: kill → start
./manage.sh --restart-frontend   # Not: kill → start
```

### Verify It Works
```bash
# After restart
./manage.sh --status
# Should show:
# ✅ MongoDB: RUNNING (port 27017)
# ✅ Backend: RUNNING (PID: XXXX, Port: 8000)
# ✅ Frontend: RUNNING (PID: XXXX, Port: 3000)

# Test the app
open http://localhost:3000
```

## Documentation References

- **[service-management-guide.md](service-management-guide.md)** - Full management guide
- **[MANAGE-QUICK-REFERENCE.md](MANAGE-QUICK-REFERENCE.md)** - Quick command reference
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[SOLUTION-PORT-CLEANUP.md](SOLUTION-PORT-CLEANUP.md)** - Solution overview

## Support

If you experience any issues:

1. Check status: `./manage.sh --status`
2. Check logs: `tail -f backend/app.log frontend/app.log`
3. Try restart: `./manage.sh restart`
4. Check ports: `lsof -i :3000` and `lsof -i :8000`
5. Manual port cleanup if needed: `lsof -ti :PORT | xargs kill -9`

---

**Your port conflict issues should now be resolved! 🚀**

The restart commands will always ensure clean ports before starting services.

