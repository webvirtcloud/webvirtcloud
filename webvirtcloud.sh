#!/usr/bin/env bash
set -e

cat << "EOF"
 __        __   _  __     ___      _    ____ _                 _ 
 \ \      / ___| |_\ \   / (_)_ __| |_ / ___| | ___  _   _  __| |
  \ \ /\ / / _ | '_ \ \ / /| | '__| __| |   | |/ _ \| | | |/ _` |
   \ V  V |  __| |_) \ V / | | |  | |_| |___| | (_) | |_| | (_| |
    \_/\_/ \___|_.__/ \_/  |_|_|   \__|\____|_|\___/ \__,_|\__,_|
                                                                        
EOF

# Start docker compose
function start_webvirtcloud() {
    ININT_DB=false

    # Check if custom.env exists
    if [ ! -f custom.env ]; then
        echo "File custom.env not found!"
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
    
    echo "Building WebVirtCloud..."
    $DOCKER_COMPOSE_COMMAND build backend --no-cache
    
    echo "Start WebVirtCloud..."
    $DOCKER_COMPOSE_COMMAND up -d
    
    # Init database
    if [ "$ININT_DB" = true ]; then
        load_initial_data
    fi
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
    echo -e "Enter your wildcard domain. By default: webvirtcloud.app"
    read -p "Enter: " domain_name
    echo "BASE_DOMAIN=${domain_name}" > custom.env
    echo "API_DOMAIN=api.${domain_name}" >> custom.env
    echo "ASSETS_DOMAIN=assets.${domain_name}" >> custom.env
    echo "CLIENT_DOMAIN=client.${domain_name}" >> custom.env
    echo "MANAGE_DOMAIN=manage.${domain_name}" >> custom.env
    echo "CONSOLE_DOMAIN=console.${domain_name}" >> custom.env
    echo -e "\nWildcard domain: "${domain_name}" added to custom.env\n"
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
help            Show this message

EOF
}

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

# Get Docker version
MIN_DOCKER_VERSION="25.0.0"
DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
# Check if Docker version meets the requirement
if check_docker_version "$DOCKER_VERSION" "$MIN_DOCKER_VERSION"; then
    echo -e "\nDocker version $DOCKER_VERSION is sufficient.\n"
else
    echo -e "\nDocker version $DOCKER_VERSION is not sufficient. Please update Docker to version $required_version or later.\n"
    exit 1
fi

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
    "restart")
        restart_webvirtcloud
        ;;
    *)
        echo "No command found."
        echo
        show_help
        ;;
esac
