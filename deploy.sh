#!/bin/bash

# Docker Build and Deploy Script for Supplier Performance Predictor

set -e

echo "🐳 Starting Docker deployment for Supplier Performance Predictor..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_success "Docker is running"

# Check if .env file exists
if [ ! -f .env ]; then
    if [ -f .env.docker.example ]; then
        print_warning ".env file not found. Creating from .env.docker.example"
        cp .env.docker.example .env
        print_warning "Please edit .env file with your actual credentials before deploying"
        exit 1
    else
        print_error ".env file not found and no template available"
        exit 1
    fi
fi

print_success "Environment file found"

# Parse command line arguments
PROFILE="default"
BUILD_ARGS=""
COMPOSE_ARGS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --production)
            PROFILE="production"
            shift
            ;;
        --with-cache)
            PROFILE="cache"
            shift
            ;;
        --with-monitoring)
            PROFILE="monitoring"
            shift
            ;;
        --build)
            BUILD_ARGS="--build"
            shift
            ;;
        --force-recreate)
            COMPOSE_ARGS="--force-recreate"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --production       Deploy with Nginx reverse proxy"
            echo "  --with-cache       Deploy with Redis cache"
            echo "  --with-monitoring  Deploy with Prometheus monitoring"
            echo "  --build           Force rebuild of Docker images"
            echo "  --force-recreate  Force recreation of containers"
            echo "  --help            Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Set compose profiles
if [ "$PROFILE" != "default" ]; then
    export COMPOSE_PROFILES="$PROFILE"
    print_status "Deploying with profile: $PROFILE"
fi

# Build and start services
print_status "Building and starting Docker services..."

if [ -n "$BUILD_ARGS" ]; then
    print_status "Building Docker images..."
    docker-compose build --no-cache
fi

print_status "Starting services..."
docker-compose up -d $COMPOSE_ARGS

# Wait for services to be healthy
print_status "Waiting for services to be ready..."
sleep 10

# Check health
if docker-compose exec -T supplier-predictor curl -f http://localhost:8001/health >/dev/null 2>&1; then
    print_success "Main application is healthy"
else
    print_error "Main application health check failed"
    print_status "Checking logs..."
    docker-compose logs supplier-predictor
    exit 1
fi

# Display service information
echo ""
print_success "Deployment completed successfully!"
echo ""
echo "📊 Service Information:"
echo "  • Main Application: http://localhost:8001"
echo "  • API Documentation: http://localhost:8001/docs"
echo "  • Health Check: http://localhost:8001/health"
echo "  • Admin Login: admin / admin123"

if [ "$PROFILE" = "production" ]; then
    echo "  • Nginx Proxy: http://localhost:80"
fi

if [ "$PROFILE" = "cache" ]; then
    echo "  • Redis Cache: localhost:6379"
fi

if [ "$PROFILE" = "monitoring" ]; then
    echo "  • Prometheus: http://localhost:9090"
fi

echo ""
echo "🔧 Management Commands:"
echo "  • View logs: docker-compose logs -f"
echo "  • Stop services: docker-compose down"
echo "  • Restart: docker-compose restart"
echo "  • Update: docker-compose pull && docker-compose up -d"
echo ""
echo "📖 Upload your supplier CSV files at: http://localhost:8001/predict"
echo ""

# Show running containers
print_status "Running containers:"
docker-compose ps
