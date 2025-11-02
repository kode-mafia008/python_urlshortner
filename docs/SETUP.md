# Setup Guide

## Prerequisites

- Docker and Docker Compose installed
- Git installed

## Step-by-Step Setup

### 1. Environment Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Update the following critical variables in `.env`:

```env
# Generate a new secret key
SECRET_KEY=your-secret-key-here

# Set strong passwords
POSTGRES_PASSWORD=your-secure-password

# Update URLs for production
BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Build and Start Services

```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d
```

### 3. Initialize Database

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser for admin access
docker-compose exec backend python manage.py createsuperuser
```

### 4. Verify Installation

Check that all services are running:

```bash
docker-compose ps
```

You should see:
- ✅ postgres (healthy)
- ✅ redis (healthy)
- ✅ backend (running)
- ✅ celery_worker (running)
- ✅ celery_beat (running)
- ✅ frontend (running)
- ✅ nginx (running)

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/docs/

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Restart specific service
docker-compose restart backend
```

### Database Connection Error

```bash
# Ensure PostgreSQL is healthy
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres
```

### Frontend Build Errors

```bash
# Access frontend container
docker-compose exec frontend sh

# Install dependencies manually
npm install

# Exit container
exit

# Rebuild
docker-compose up --build frontend
```

### Celery Not Processing Tasks

```bash
# Check Celery worker status
docker-compose logs celery_worker

# Restart worker
docker-compose restart celery_worker celery_beat
```

## Development Workflow

### Making Backend Changes

```bash
# Backend code changes are auto-reloaded in DEBUG mode
# If you add new dependencies:
docker-compose exec backend pip install <package>
docker-compose exec backend pip freeze > requirements.txt
docker-compose restart backend
```

### Making Frontend Changes

```bash
# Frontend has hot-reload enabled
# If you add new dependencies:
docker-compose exec frontend npm install <package>
docker-compose restart frontend
```

### Running Database Migrations

```bash
# Create migration
docker-compose exec backend python manage.py makemigrations

# Apply migration
docker-compose exec backend python manage.py migrate
```

### Accessing Databases

```bash
# PostgreSQL
docker-compose exec postgres psql -U postgres -d urlshortener

# Redis
docker-compose exec redis redis-cli
```

## Stopping Services

```bash
# Stop all services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers, volumes, and networks
docker-compose down -v
```

## Production Deployment

### 1. Update Environment

```env
DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
BASE_URL=https://yourdomain.com
```

### 2. Collect Static Files

```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

### 3. Configure SSL/TLS

Update `nginx/nginx.conf` to include SSL certificates:

```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ...
}
```

### 4. Security Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS
- [ ] Use strong database passwords
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up monitoring and logging
- [ ] Configure backups

## Useful Commands

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Execute Django management command
docker-compose exec backend python manage.py <command>

# Access backend shell
docker-compose exec backend python manage.py shell

# Run tests
docker-compose exec backend python manage.py test

# Clean up Docker
docker system prune -a
```
