# Docker Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the Supplier Performance Predictor using Docker containers.

## Quick Start

### 1. Single Container Deployment (Recommended for Development)

```bash
# Clone the repository
git clone <your-repo-url>
cd supplier-performance-predictor

# Build the Docker image
docker build -t supplier-predictor:latest .

# Run the container
docker run -d \
  --name supplier-predictor \
  -p 8002:8001 \
  -e AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
  -e AZURE_OPENAI_API_KEY="your-api-key" \
  -e LANGCHAIN_API_KEY="your-langsmith-key" \
  supplier-predictor:latest

# Check container status
docker ps
docker logs supplier-predictor

# Access the application
curl http://localhost:8002/health
# Browse to http://localhost:8002 for frontend
# Browse to http://localhost:8002/docs for API documentation
```

### 2. Production Deployment with Docker Compose

```bash
# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps
docker-compose logs

# Access via nginx reverse proxy
# Frontend: http://localhost
# API: http://localhost/docs
```

## Container Architecture

### Single Container
- **Base Image**: python:3.9-slim
- **Security**: Non-root user execution
- **Health Checks**: Built-in health monitoring
- **Optimization**: Multi-stage build for smaller image size

### Docker Compose Stack
- **Application**: FastAPI backend with frontend
- **Database**: MySQL 8.0 (optional, SQLite by default)
- **Reverse Proxy**: Nginx for load balancing and SSL termination
- **Networking**: Isolated Docker network for security

## Environment Variables

### Required
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL

### Optional
- `LANGCHAIN_API_KEY`: For LangSmith observability
- `SECRET_KEY`: For JWT token security
- `DEBUG`: Set to true for development
- `LOG_LEVEL`: INFO, DEBUG, WARNING, ERROR

## Container Management

### Starting Services
```bash
# Single container
docker start supplier-predictor

# Docker Compose
docker-compose up -d
```

### Stopping Services
```bash
# Single container
docker stop supplier-predictor

# Docker Compose
docker-compose down
```

### Viewing Logs
```bash
# Single container
docker logs -f supplier-predictor

# Docker Compose
docker-compose logs -f
docker-compose logs -f app  # Specific service
```

### Updating the Application
```bash
# Single container
docker pull supplier-predictor:latest
docker stop supplier-predictor && docker rm supplier-predictor
docker run -d --name supplier-predictor -p 8002:8001 supplier-predictor:latest

# Docker Compose
docker-compose pull
docker-compose up -d --force-recreate
```

## Troubleshooting

### Common Issues

1. **Container exits immediately**
   ```bash
   docker logs supplier-predictor
   # Check for missing environment variables or dependency issues
   ```

2. **Port conflicts**
   ```bash
   # Change host port
   docker run -p 8003:8001 supplier-predictor:latest
   ```

3. **Database connection issues**
   ```bash
   # Check database container status
   docker-compose ps
   docker-compose logs db
   ```

### Health Checks
```bash
# Check container health
docker inspect supplier-predictor | grep Health

# Test health endpoint
curl http://localhost:8002/health
```

### Performance Monitoring
```bash
# View resource usage
docker stats supplier-predictor

# View container processes
docker exec supplier-predictor ps aux
```

## Security Considerations

### Container Security
- Non-root user execution
- Minimal base image (python:3.9-slim)
- No unnecessary packages
- Health checks for monitoring

### Network Security
- Isolated Docker networks
- Environment variable injection
- No hardcoded secrets

### Production Recommendations
- Use secrets management (Docker Secrets, Kubernetes Secrets)
- Enable container scanning
- Regular security updates
- SSL/TLS termination at reverse proxy

## Scaling

### Horizontal Scaling
```bash
# Scale with Docker Compose
docker-compose up -d --scale app=3

# Manual scaling
docker run -d --name supplier-predictor-2 -p 8003:8001 supplier-predictor:latest
docker run -d --name supplier-predictor-3 -p 8004:8001 supplier-predictor:latest
```

### Load Balancing
- Nginx reverse proxy included in Docker Compose
- Configure upstream servers for multiple instances
- Health check integration

## Backup and Recovery

### Database Backup
```bash
# SQLite backup (single container)
docker exec supplier-predictor cp /app/supplier_predictor.db /tmp/
docker cp supplier-predictor:/tmp/supplier_predictor.db ./backup/

# MySQL backup (Docker Compose)
docker-compose exec db mysqldump -u root -p supplier_db > backup.sql
```

### Configuration Backup
```bash
# Backup environment and configuration
cp .env backup/
cp docker-compose.yml backup/
```

## Monitoring and Observability

### Container Metrics
- Built-in Docker stats
- Health check endpoints
- Application logs

### LangSmith Integration
- AI operation tracing
- Performance analytics
- Cost monitoring
- Error tracking

### Log Management
```bash
# Configure log rotation
docker run --log-driver=json-file --log-opt max-size=10m --log-opt max-file=3 \
  supplier-predictor:latest
```

## Support

For issues and questions:
- Check container logs: `docker logs supplier-predictor`
- Review health endpoint: `curl http://localhost:8002/health`
- Validate environment variables
- Check network connectivity
- Review Docker Compose service dependencies
