#!/bin/bash
# Quick Start Script for Intelligent Customer Service Analytics Platform

set -e

echo "=================================="
echo "Analytics Platform - Quick Start"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker not found. Installing Docker...${NC}"
    # Docker installation instructions
    echo "Please install Docker from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose not found. Installing Docker Compose...${NC}"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${BLUE}✓ Docker and Docker Compose found${NC}"
echo ""

# Option to choose deployment method
echo "Select deployment method:"
echo "1) Docker (Recommended - All services)"
echo "2) Manual (Local development)"
echo "3) Exit"
echo ""
read -p "Enter option (1/2/3): " choice

case $choice in
    1)
        echo -e "${BLUE}Starting Docker deployment...${NC}"
        echo ""
        
        # Start Docker containers
        echo "Building docker images..."
        docker-compose build
        
        echo -e "${GREEN}✓ Docker images built${NC}"
        echo ""
        
        echo "Starting containers..."
        docker-compose up -d
        
        echo -e "${GREEN}✓ Containers started${NC}"
        echo ""
        
        # Wait for services to start
        echo "Waiting for services to start (30 seconds)..."
        sleep 30
        
        # Check health
        echo -e "${BLUE}Checking service health...${NC}"
        if curl -s http://localhost:8000/health > /dev/null; then
            echo -e "${GREEN}✓ API is running${NC}"
        else
            echo -e "${YELLOW}⚠ API not responding yet${NC}"
        fi
        
        echo ""
        echo -e "${GREEN}=================================="
        echo "✓ Platform is ready!${NC}"
        echo "=================================="
        echo ""
        echo "Access the platform:"
        echo -e "${BLUE}Frontend:     http://localhost:3000${NC}"
        echo -e "${BLUE}API:          http://localhost:8000${NC}"
        echo -e "${BLUE}API Docs:     http://localhost:8000/docs${NC}"
        echo -e "${BLUE}Streamlit:    http://localhost:8501${NC}"
        echo ""
        echo "Default credentials:"
        echo "  - Create account on first login"
        echo ""
        echo "Stop services:     docker-compose down"
        echo "View logs:         docker-compose logs -f"
        echo ""
        ;;
    
    2)
        echo -e "${BLUE}Starting manual deployment...${NC}"
        echo ""
        
        # Check Python version
        if ! command -v python3 &> /dev/null; then
            echo -e "${YELLOW}Python 3 not found. Please install Python 3.11+${NC}"
            echo "Download from: https://www.python.org/downloads/"
            exit 1
        fi
        
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
        echo ""
        
        # Check Node.js version
        if ! command -v node &> /dev/null; then
            echo -e "${YELLOW}Node.js not found. Please install Node.js 18+${NC}"
            echo "Download from: https://nodejs.org/"
            exit 1
        fi
        
        NODE_VERSION=$(node --version)
        echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
        echo ""
        
        # Check PostgreSQL
        if ! command -v psql &> /dev/null; then
            echo -e "${YELLOW}PostgreSQL not found. Please install PostgreSQL 15+${NC}"
            echo "Download from: https://www.postgresql.org/download/"
            exit 1
        fi
        
        echo -e "${GREEN}✓ PostgreSQL found${NC}"
        echo ""
        
        # Setup backend
        echo -e "${BLUE}Setting up backend...${NC}"
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        
        if [ ! -f .env ]; then
            cp .env.example .env
            echo -e "${YELLOW}⚠ .env file created. Please edit with your settings.${NC}"
        fi
        
        # Setup database
        echo -e "${BLUE}Setting up database...${NC}"
        createdb customer_analytics 2>/dev/null || true
        python3 -c "from database import create_tables; create_tables()"
        echo -e "${GREEN}✓ Database initialized${NC}"
        echo ""
        
        # Start backend
        echo -e "${BLUE}Starting backend server...${NC}"
        python3 run_api.py &
        BACKEND_PID=$!
        sleep 3
        
        # Start frontend
        echo -e "${BLUE}Setting up frontend...${NC}"
        cd frontend
        npm install
        npm start &
        FRONTEND_PID=$!
        
        echo ""
        echo -e "${GREEN}=================================="
        echo "✓ Platform is running!${NC}"
        echo "=================================="
        echo ""
        echo "Access the platform:"
        echo -e "${BLUE}Frontend:     http://localhost:3000${NC}"
        echo -e "${BLUE}API:          http://localhost:8000${NC}"
        echo -e "${BLUE}API Docs:     http://localhost:8000/docs${NC}"
        echo ""
        echo "Process IDs:"
        echo "  Backend: $BACKEND_PID"
        echo "  Frontend: $FRONTEND_PID"
        echo ""
        echo "Press CTRL+C to stop services"
        echo ""
        
        wait
        ;;
    
    3)
        echo "Exiting..."
        exit 0
        ;;
    
    *)
        echo -e "${YELLOW}Invalid option${NC}"
        exit 1
        ;;
esac