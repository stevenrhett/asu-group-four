#!/bin/bash
# Job Portal Management Script
# Unified script to manage MongoDB, Backend, and Frontend services
# Follows BMAD methodology for systematic development workflows

set -e

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# PID file locations
BACKEND_PID_FILE=".backend.pid"
FRONTEND_PID_FILE=".frontend.pid"

# Log file locations
BACKEND_LOG_FILE="backend/app.log"
FRONTEND_LOG_FILE="frontend/app.log"

#------------------------------------------------------------------------------
# Helper Functions
#------------------------------------------------------------------------------

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  Job Portal - Service Manager${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

#------------------------------------------------------------------------------
# MongoDB Management
#------------------------------------------------------------------------------

check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running!"
        print_info "Please start Docker Desktop and try again."
        exit 1
    fi
}

start_mongodb() {
    print_info "Starting MongoDB..."
    check_docker
    
    if docker ps | grep -q job-portal-mongo; then
        print_warning "MongoDB is already running"
        return 0
    fi
    
    if docker ps -a | grep -q job-portal-mongo; then
        docker start job-portal-mongo > /dev/null 2>&1
    else
        docker run -d \
            --name job-portal-mongo \
            -p 27017:27017 \
            mongo:latest > /dev/null 2>&1
    fi
    
    # Wait for MongoDB to be ready
    sleep 3
    
    if docker ps | grep -q job-portal-mongo; then
        print_success "MongoDB running on localhost:27017"
    else
        print_error "MongoDB failed to start"
        exit 1
    fi
}

stop_mongodb() {
    print_info "Stopping MongoDB..."
    if docker ps | grep -q job-portal-mongo; then
        docker stop job-portal-mongo > /dev/null 2>&1
        print_success "MongoDB stopped"
    else
        print_warning "MongoDB is not running"
    fi
}

mongodb_status() {
    if docker ps | grep -q job-portal-mongo; then
        print_success "MongoDB: RUNNING (port 27017)"
    elif docker ps -a | grep -q job-portal-mongo; then
        print_warning "MongoDB: STOPPED"
    else
        print_info "MongoDB: NOT CREATED"
    fi
}

#------------------------------------------------------------------------------
# Port Cleanup Functions
#------------------------------------------------------------------------------

cleanup_port() {
    local PORT=$1
    local SERVICE_NAME=$2
    
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        local PIDS=$(lsof -ti :$PORT 2>/dev/null)
        if [ ! -z "$PIDS" ]; then
            print_info "Cleaning up processes on port $PORT for $SERVICE_NAME..."
            echo "$PIDS" | xargs kill -9 2>/dev/null || true
            sleep 1
            print_success "Port $PORT cleared"
        fi
    fi
}

force_cleanup_backend() {
    print_info "Force cleaning backend processes..."
    
    # Kill by port
    cleanup_port 8000 "Backend"
    
    # Kill any remaining uvicorn processes
    pkill -9 -f "uvicorn.*app.main" 2>/dev/null || true
    
    # Clean PID file
    rm -f "$BACKEND_PID_FILE"
}

force_cleanup_frontend() {
    print_info "Force cleaning frontend processes..."
    
    # Kill by ports (3000 and 3001 in case it moved)
    cleanup_port 3000 "Frontend"
    cleanup_port 3001 "Frontend"
    
    # Kill any remaining Next.js processes
    pkill -9 -f "next dev" 2>/dev/null || true
    
    # Clean PID file
    rm -f "$FRONTEND_PID_FILE"
}

#------------------------------------------------------------------------------
# Backend Management
#------------------------------------------------------------------------------

start_backend() {
    print_info "Starting Backend..."
    
    # Check if port 8000 is already in use
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        EXISTING_PID=$(lsof -ti :8000 2>/dev/null | head -1)
        print_error "Port 8000 is already in use (PID: $EXISTING_PID)"
        print_info "Use './manage.sh restart' to automatically clean up and restart"
        print_info "Or manually kill: kill -9 $EXISTING_PID"
        return 1
    fi
    
    # Check if already running via PID file
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
            print_warning "Backend is already running (PID: $BACKEND_PID)"
            return 0
        else
            rm -f "$BACKEND_PID_FILE"
        fi
    fi
    
    # Ensure MongoDB is running
    if ! docker ps | grep -q job-portal-mongo; then
        start_mongodb
    fi
    
    # Check if virtual environment exists
    if [ ! -d "backend/venv" ]; then
        print_info "Creating Python virtual environment..."
        cd backend
        python3 -m venv venv
        cd ..
    fi
    
    # Check if requirements are installed
    print_info "Ensuring dependencies are installed..."
    cd backend
    source venv/bin/activate
    pip install -q -r requirements.txt
    cd ..
    
    # Start backend in background
    print_info "Starting FastAPI server on port 8000..."
    cd backend
    nohup bash -c "source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" > "../$BACKEND_LOG_FILE" 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    echo "$BACKEND_PID" > "$BACKEND_PID_FILE"
    
    # Wait a moment and verify it started
    sleep 2
    if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
        print_success "Backend running (PID: $BACKEND_PID, Port: 8000)"
        print_info "Backend logs: $BACKEND_LOG_FILE"
        print_info "API Docs: http://localhost:8000/docs"
    else
        print_error "Backend failed to start. Check logs: $BACKEND_LOG_FILE"
        rm -f "$BACKEND_PID_FILE"
        exit 1
    fi
}

stop_backend() {
    print_info "Stopping Backend..."
    
    local STOPPED=false
    
    # Try to stop via PID file first
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
            kill "$BACKEND_PID" 2>/dev/null || true
            sleep 2
            # Force kill if still running
            if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
                kill -9 "$BACKEND_PID" 2>/dev/null || true
            fi
            STOPPED=true
        fi
        rm -f "$BACKEND_PID_FILE"
    fi
    
    # Also check and clean up any processes on port 8000
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        cleanup_port 8000 "Backend"
        STOPPED=true
    fi
    
    if [ "$STOPPED" = true ]; then
        print_success "Backend stopped"
    else
        print_warning "Backend was not running"
    fi
}

backend_status() {
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
            print_success "Backend: RUNNING (PID: $BACKEND_PID, Port: 8000)"
        else
            print_error "Backend: STOPPED (stale PID file)"
            rm -f "$BACKEND_PID_FILE"
        fi
    else
        print_warning "Backend: STOPPED"
    fi
}

#------------------------------------------------------------------------------
# Frontend Management
#------------------------------------------------------------------------------

start_frontend() {
    print_info "Starting Frontend..."
    
    # Check if port 3000 is already in use
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        EXISTING_PID=$(lsof -ti :3000 2>/dev/null | head -1)
        print_error "Port 3000 is already in use (PID: $EXISTING_PID)"
        print_info "Use './manage.sh restart' to automatically clean up and restart"
        print_info "Or manually kill: kill -9 $EXISTING_PID"
        return 1
    fi
    
    # Check if already running via PID file
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
            print_warning "Frontend is already running (PID: $FRONTEND_PID)"
            return 0
        else
            rm -f "$FRONTEND_PID_FILE"
        fi
    fi
    
    # Check if node_modules exists
    if [ ! -d "frontend/node_modules" ]; then
        print_info "Installing npm dependencies..."
        cd frontend
        npm install
        cd ..
    fi
    
    # Start frontend in background
    print_info "Starting Next.js development server on port 3000..."
    cd frontend
    nohup npm run dev > "../$FRONTEND_LOG_FILE" 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    echo "$FRONTEND_PID" > "$FRONTEND_PID_FILE"
    
    # Wait a moment and verify it started
    sleep 3
    if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
        print_success "Frontend running (PID: $FRONTEND_PID, Port: 3000)"
        print_info "Frontend logs: $FRONTEND_LOG_FILE"
        print_info "Application URL: http://localhost:3000"
    else
        print_error "Frontend failed to start. Check logs: $FRONTEND_LOG_FILE"
        rm -f "$FRONTEND_PID_FILE"
        exit 1
    fi
}

stop_frontend() {
    print_info "Stopping Frontend..."
    
    local STOPPED=false
    
    # Try to stop via PID file first
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
            # Kill the process group to ensure all child processes are killed
            pkill -P "$FRONTEND_PID" 2>/dev/null || true
            kill "$FRONTEND_PID" 2>/dev/null || true
            sleep 2
            # Force kill if still running
            if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
                kill -9 "$FRONTEND_PID" 2>/dev/null || true
            fi
            STOPPED=true
        fi
        rm -f "$FRONTEND_PID_FILE"
    fi
    
    # Also check and clean up any processes on ports 3000 and 3001
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        cleanup_port 3000 "Frontend"
        STOPPED=true
    fi
    if lsof -Pi :3001 -sTCP:LISTEN -t >/dev/null 2>&1; then
        cleanup_port 3001 "Frontend (alt port)"
        STOPPED=true
    fi
    
    if [ "$STOPPED" = true ]; then
        print_success "Frontend stopped"
    else
        print_warning "Frontend was not running"
    fi
}

frontend_status() {
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
            print_success "Frontend: RUNNING (PID: $FRONTEND_PID, Port: 3000)"
        else
            print_error "Frontend: STOPPED (stale PID file)"
            rm -f "$FRONTEND_PID_FILE"
        fi
    else
        print_warning "Frontend: STOPPED"
    fi
}

#------------------------------------------------------------------------------
# Combined Operations
#------------------------------------------------------------------------------

start_all() {
    print_header
    print_info "Starting all services..."
    echo ""
    start_mongodb
    echo ""
    start_backend
    echo ""
    start_frontend
    echo ""
    print_success "All services started successfully!"
    echo ""
    print_info "Access Points:"
    echo "  • Frontend:  http://localhost:3000"
    echo "  • Backend:   http://localhost:8000"
    echo "  • API Docs:  http://localhost:8000/docs"
    echo ""
}

stop_all() {
    print_header
    print_info "Stopping all services..."
    echo ""
    stop_frontend
    echo ""
    stop_backend
    echo ""
    stop_mongodb
    echo ""
    print_success "All services stopped successfully!"
    echo ""
}

restart_all() {
    print_header
    print_info "Restarting all services..."
    echo ""
    
    # Force cleanup of all services
    print_info "Cleaning up all services..."
    echo ""
    force_cleanup_frontend
    echo ""
    force_cleanup_backend
    echo ""
    
    # MongoDB doesn't need cleanup (Docker managed)
    if docker ps | grep -q job-portal-mongo 2>/dev/null; then
        print_info "Restarting MongoDB..."
        docker restart job-portal-mongo > /dev/null 2>&1
        print_success "MongoDB restarted"
        sleep 2
    fi
    
    echo ""
    print_info "Starting all services fresh..."
    echo ""
    start_mongodb
    echo ""
    start_backend
    echo ""
    start_frontend
    echo ""
    print_success "All services restarted successfully!"
    echo ""
    print_info "Access Points:"
    echo "  • Frontend:  http://localhost:3000"
    echo "  • Backend:   http://localhost:8000"
    echo "  • API Docs:  http://localhost:8000/docs"
    echo ""
}

restart_backend() {
    print_header
    print_info "Restarting backend..."
    echo ""
    
    # Force cleanup to ensure ports are free
    force_cleanup_backend
    echo ""
    
    # Ensure MongoDB is running
    if ! docker ps | grep -q job-portal-mongo 2>/dev/null; then
        start_mongodb
        echo ""
    fi
    
    start_backend
    echo ""
    print_success "Backend restarted successfully!"
    echo ""
}

restart_frontend() {
    print_header
    print_info "Restarting frontend..."
    echo ""
    
    # Force cleanup to ensure ports are free
    force_cleanup_frontend
    echo ""
    
    start_frontend
    echo ""
    print_success "Frontend restarted successfully!"
    echo ""
}

show_status() {
    print_header
    print_info "Service Status:"
    echo ""
    mongodb_status
    backend_status
    frontend_status
    echo ""
}

show_help() {
    print_header
    echo "Usage: ./manage.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  ${GREEN}start, --start-all${NC}           Start all services (MongoDB, Backend, Frontend)"
    echo "  ${GREEN}stop, --stop-all${NC}             Stop all services"
    echo "  ${GREEN}restart, --restart-all${NC}       Restart all services"
    echo ""
    echo "  ${GREEN}--start-backend${NC}              Start backend only"
    echo "  ${GREEN}--start-frontend${NC}             Start frontend only"
    echo "  ${GREEN}--stop-backend${NC}               Stop backend only"
    echo "  ${GREEN}--stop-frontend${NC}              Stop frontend only"
    echo "  ${GREEN}--restart-backend${NC}            Restart backend only"
    echo "  ${GREEN}--restart-frontend${NC}           Restart frontend only"
    echo ""
    echo "  ${GREEN}--status${NC}                     Show status of all services"
    echo "  ${GREEN}--help, -h${NC}                   Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./manage.sh start              # Start everything"
    echo "  ./manage.sh --restart-backend  # Restart just the backend"
    echo "  ./manage.sh --status           # Check what's running"
    echo ""
    echo "Troubleshooting:"
    echo "  ${GREEN}./manage.sh restart${NC}          # Restart with automatic cleanup"
    echo ""
    echo "Logs:"
    echo "  Backend:  $BACKEND_LOG_FILE"
    echo "  Frontend: $FRONTEND_LOG_FILE"
    echo ""
}

#------------------------------------------------------------------------------
# Main Command Handler
#------------------------------------------------------------------------------

if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

case "$1" in
    start|--start|--start-all)
        start_all
        ;;
    stop|--stop|--stop-all)
        stop_all
        ;;
    restart|--restart|--restart-all)
        restart_all
        ;;
    --start-backend)
        print_header
        start_mongodb
        echo ""
        start_backend
        echo ""
        ;;
    --start-frontend)
        print_header
        start_frontend
        echo ""
        ;;
    --stop-backend)
        print_header
        stop_backend
        echo ""
        ;;
    --stop-frontend)
        print_header
        stop_frontend
        echo ""
        ;;
    --restart-backend)
        restart_backend
        ;;
    --restart-frontend)
        restart_frontend
        ;;
    --status)
        show_status
        ;;
    --help|-h|help)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

