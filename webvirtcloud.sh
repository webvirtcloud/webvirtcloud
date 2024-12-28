#!/usr/bin/env bash
set -e

cat << "EOF"
 __        __   _  __     ___      _    ____ _                 _ 
 \ \      / ___| |_\ \   / (_)_ __| |_ / ___| | ___  _   _  __| |
  \ \ /\ / / _ | '_ \ \ / /| | '__| __| |   | |/ _ \| | | |/ _` |
   \ V  V |  __| |_) \ V / | | |  | |_| |___| | (_) | |_| | (_| |
    \_/\_/ \___|_.__/ \_/  |_|_|   \__|\____|_|\___/ \__,_|\__,_|
                                                                        
EOF

# Define minimum Docker version
MIN_DOCKER_VERSION="25.0.0"
DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "\nDocker not found! Please install Docker first.\n"
    exit 1
fi

# Check docker version function
check_docker_version() {
  # Split version strings into arrays
  IFS='.' read -r -a current_version <<< "$1"
  IFS='.' read -r -a min_version <<< "$2"
  for i in 0 1 2; do
    # Check (major, minor, patch)
    if [[ ${current_version[i]} -gt ${min_version[i]} ]]; then
      return 0
    elif [[ ${current_version[i]} -lt ${min_version[i]} ]]; then
      return 1
    fi
  done
  return 0
}

# Check if Docker version meets the requirement
if check_docker_version "$DOCKER_VERSION" "$MIN_DOCKER_VERSION"; then
    echo -e "\nDocker version $DOCKER_VERSION is sufficient.\n"
else
    echo -e "\nDocker version $DOCKER_VERSION is not sufficient. Please update Docker to version $MIN_DOCKER_VERSION or later.\n"
    exit 1
fi

# Check if Docker Compose is installed
if docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE_COMMAND="docker compose"
elif command -v docker-compose > /dev/null 2>&1; then
    DOCKER_COMPOSE_COMMAND="docker-compose"
else
    echo "Neither 'docker compose' nor 'docker-compose' command found."
    exit 1
fi

# Start docker compose
function start_webvirtcloud() {
    ININT_DB=false

    # Check if env.local exists
    if [ ! -f env.local ]; then
        echo "File env.local not found!"
        echo -e "\nRun '$0 env' first\n"
        exit 1
    fi

    # Check submodules
    if [ -z "$(ls -A "webvirtbackend")" ]; then
        init_submodules
    fi

    # Check if .mysql directory exists
    if [ ! -d ".mysql" ]; then
        ININT_DB=true
    fi
    
    echo "Building WebVirtCloud frontend..."
    $DOCKER_COMPOSE_COMMAND build frontend --no-cache

    echo "Building WebVirtCloud backend..."
    $DOCKER_COMPOSE_COMMAND build backend --no-cache
    
    echo "Start WebVirtCloud..."
    $DOCKER_COMPOSE_COMMAND up -d
    
    # Init database
    if [ "$ININT_DB" = true ]; then
        create_default_admin
        load_initial_data
    fi
}

function create_default_admin() {
    echo "Creating 'admin@webvirt.cloud' user..."
    $DOCKER_COMPOSE_COMMAND exec backend python manage.py loaddata account/fixtures/admin.json
}

# Load initial data
function load_initial_data() {
    echo "Loading initial data..."
    $DOCKER_COMPOSE_COMMAND exec backend python manage.py loaddata initial_data
}

# Init and update submodules
function init_submodules() {
    echo "Init submodules..."
    git submodule update --init --recursive
}

# Restart docker compose
function restart_webvirtcloud() {
    echo "Restarting WebVirtCloud..."
    $DOCKER_COMPOSE_COMMAND restart
}

# Stop docker compose
function stop_webvirtcloud() {
    echo "Stop WebVirtCloud..."
    $DOCKER_COMPOSE_COMMAND down
}

# Pull latest changes
function git_pull() {
    echo "Pulling latest changes..."
    git pull
    git submodule update
}

# Add base domain to custom.env
function add_to_custom_env() {
    echo -e "Enter your domain or IP address (only HTTP). Default: localhost"
    read -p "Enter: " DOMAIN_NAME
    if [ -z "$DOMAIN_NAME" ]; then
        DOMAIN_NAME="localhost"
    fi
    echo "DOMAIN_NAME=${DOMAIN_NAME}" > env.local
    echo -e "\nDomain: '"${DOMAIN_NAME}"' added to env.local\n"

    echo -e "Do you want to enable show prices in sizes on client side? (yes/no). Default: no"
    read -p "Enter: " ENABLE_PRICE
    if [ "$ENABLE_PRICE" = "yes" ]; then
        echo "VITE_DISPLAY_PRICES=true" >> env.local
        echo -e "\nShow prices enabled on client side\n"
    else
        echo -e "\nShow prices is not enabled on client side\n"
    fi

    echo -e "Do you want to enable Load Balancer features on client side? (yes/no). Default: no"
    read -p "Enter: " ENABLE_LB
    if [ "$ENABLE_LB" = "yes" ]; then
        echo "VITE_LOADBALANCER=true" >> env.local
        echo -e "\nLoad Balancer enabled on client side\n"
    else
        echo -e "\nLoad Balancer is not enabled on client side\n"
    fi
}

# Show help function
function show_help() {
cat << "EOF"
Available commands:

env             Configure custom.env
start           Start WebVirtCloud
restart         Restart WebVirtCloud
stop            Stop WebVirtCloud
update          Update WebVirtCloud
loaddata        Load initial data
help            Show this message

EOF
}

# Run functions
case "$1" in
    "help")
        show_help
        ;;
    "env")
        add_to_custom_env
        ;;
    "start")
        start_webvirtcloud
        ;;
    "stop")
        stop_webvirtcloud
        ;;
    "update")
        stop_webvirtcloud
        git_pull
        start_webvirtcloud
        ;;
    "loaddata")
        load_initial_data
        ;;
    "restart")
        restart_webvirtcloud
        ;;
    *)
        echo "No command found."
        echo
        show_help
        ;;
esac