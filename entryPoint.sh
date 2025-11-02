#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${BLUE}"
cat << "EOF"
╦ ╦╦═╗╦    ╔═╗╦ ╦╔═╗╦═╗╔╦╗╔═╗╔╗╔╔═╗╦═╗
║ ║╠╦╝║    ╚═╗╠═╣║ ║╠╦╝ ║ ║╣ ║║║║╣ ╠╦╝
╚═╝╩╚═╩═╝  ╚═╝╩ ╩╚═╝╩╚═ ╩ ╚═╝╝╚╝╚═╝╩╚═
EOF
echo -e "${NC}"

echo -e "${GREEN}Welcome to URL Shortener Setup!${NC}"
echo ""

# Function to check if .env exists
check_env_file() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}⚠️  .env file not found!${NC}"
        echo -e "${BLUE}Creating .env from .env.example...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created${NC}"
        echo ""
    else
        echo -e "${GREEN}✓ .env file found${NC}"
        echo ""
    fi
}

# Function to start development mode
start_dev_mode() {
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🔥 Starting in DEVELOPMENT MODE${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}Features enabled:${NC}"
    echo "  ✓ Hot-reload for backend (Django)"
    echo "  ✓ Hot-reload for frontend (Next.js)"
    echo "  ✓ Volume mounts for live code changes"
    echo "  ✓ Debug mode enabled"
    echo ""
    
    echo -e "${BLUE}Stopping existing containers...${NC}"
    docker-compose down 2>/dev/null
    
    echo -e "${BLUE}Starting containers...${NC}"
    docker-compose -f docker-compose.dev.yml up -d --build
    
    sleep 5
    
    read -p "$(echo -e ${YELLOW}Do you want to run migrations? [y/N]:${NC} )" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate
    fi
    
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ Development environment is ready!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}Access your application:${NC}"
    echo "  • Frontend:       http://localhost/"
    echo "  • Backend API:    http://localhost/api/"
    echo "  • API Docs:       http://localhost/api/docs/"
    echo ""
    echo -e "${YELLOW}💡 Code changes will auto-reload!${NC}"
    echo -e "${YELLOW}💡 View logs: docker-compose -f docker-compose.dev.yml logs -f${NC}"
    echo ""
}

# Function to start production mode
start_prod_mode() {
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🚀 Starting in PRODUCTION MODE${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}Features enabled:${NC}"
    echo "  ✓ Optimized builds"
    echo "  ✓ Gunicorn WSGI server"
    echo "  ✓ Static file serving"
    echo ""
    
    echo -e "${BLUE}Stopping existing containers...${NC}"
    docker-compose -f docker-compose.dev.yml down 2>/dev/null
    docker-compose down
    
    echo -e "${BLUE}Building and starting containers...${NC}"
    docker-compose up -d --build
    
    sleep 5
    
    echo -e "${BLUE}Running migrations...${NC}"
    docker-compose exec backend python manage.py migrate
    
    read -p "$(echo -e ${YELLOW}Create superuser? [y/N]:${NC} )" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose exec backend python manage.py createsuperuser
    fi
    
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ Production environment is ready!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}Access your application:${NC}"
    echo "  • Frontend:       http://localhost/"
    echo "  • Backend API:    http://localhost/api/"
    echo "  • API Docs:       http://localhost/api/docs/"
    echo ""
}

# Main menu
show_menu() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}        Select an option:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "  1) 🔥 Development Mode (Hot-Reload)"
    echo "  2) 🚀 Production Mode"
    echo "  3) 🛑 Stop All Services"
    echo "  4) 🚪 Exit"
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

check_env_file

while true; do
    show_menu
    read -p "Enter your choice [1-4]: " choice
    echo ""
    
    case $choice in
        1)
            start_dev_mode
            break
            ;;
        2)
            start_prod_mode
            break
            ;;
        3)
            echo -e "${BLUE}Stopping all services...${NC}"
            docker-compose -f docker-compose.dev.yml down 2>/dev/null
            docker-compose down
            echo -e "${GREEN}✓ All services stopped${NC}"
            exit 0
            ;;
        4)
            echo -e "${GREEN}Goodbye! 👋${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please choose 1-4.${NC}"
            echo ""
            ;;
    esac
done