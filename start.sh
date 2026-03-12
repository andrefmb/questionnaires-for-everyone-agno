#!/bin/bash

# Questionnaires for Everyone - Start Script
# Automates Virtual Environment, Server, and Client startup.

# Exit on error
set -e

# Get the script directory
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_DIR="$ROOT_DIR/questionnaires-for-everyone-agno-server"
CLIENT_DIR="$ROOT_DIR/questionnaires-for-everyone-agno-main"

echo "------------------------------------------------"
echo "🚀 Starting Questionnaires for Everyone"
echo "------------------------------------------------"

# Function to Cleanup background processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    [ -n "$SERVER_PID" ] && kill $SERVER_PID 2>/dev/null || true
    [ -n "$CLIENT_PID" ] && kill $CLIENT_PID 2>/dev/null || true
    exit
}

trap cleanup SIGINT SIGTERM

# 1. Setup/Start Server
echo "📡 [1/2] Starting Backend Server..."
cd "$SERVER_DIR"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment and installing dependencies..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

echo "Running Server in background (port 5001)..."
# Using python directly from venv to ensure correct environment
./venv/bin/python app.py > server_log.txt 2>&1 &
SERVER_PID=$!

# Give the server a second to start
sleep 2

# 2. Setup/Start Client
echo "💻 [2/2] Starting Frontend Client..."
cd "$CLIENT_DIR"

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies (npm install)..."
    npm install
fi

echo "Running Frontend (Vite)..."
npm run dev &
CLIENT_PID=$!

echo "------------------------------------------------"
echo "✅ Everything is running!"
echo "------------------------------------------------"
echo "🔗 Backend: http://localhost:5001"
echo "📝 Server logs: $SERVER_DIR/server_log.txt"
echo "------------------------------------------------"
echo "⚠️  Keep this terminal open. Press Ctrl+C to stop everything."

# Wait for background processes
wait
