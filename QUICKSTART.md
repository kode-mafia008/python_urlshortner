# Quick Start Guide

Get your URL shortener running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed on your system
- 4GB+ RAM available
- Ports 3000, 8000, 5432, 6379, 80 available

## Steps

### 1. Configure Environment (30 seconds)

```bash
# Copy environment template
cp .env.example .env

# Optional: Edit .env to customize settings
# nano .env
```

**Important**: For production, generate a secure SECRET_KEY:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Start All Services (2-3 minutes)

```bash
# Build and start all containers
docker-compose up -d --build
```

This command will:
- ✅ Build backend Docker image
- ✅ Build frontend Docker image  
- ✅ Start PostgreSQL database
- ✅ Start Redis cache
- ✅ Start Django backend
- ✅ Start Celery worker
- ✅ Start Celery beat scheduler
- ✅ Start Next.js frontend
- ✅ Start Nginx reverse proxy

### 3. Initialize Database (1 minute)

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create admin user (follow prompts)
docker-compose exec backend python manage.py createsuperuser
```

### 4. Access Your Application

🎉 **Done!** Your URL shortener is now running:

- **Frontend (User Interface)**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/
- **Alternative API Docs**: http://localhost:8000/api/redoc/

## Testing the Application

### Create Your First Short URL

1. Open http://localhost:3000
2. Enter a long URL (e.g., `https://www.example.com/very/long/url`)
3. Click "Shorten URL"
4. Copy your short URL and test it!

### Using the API

```bash
# Create a short URL
curl -X POST http://localhost:8000/api/urls/ \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://www.example.com/very/long/url",
    "title": "Example Site"
  }'

# Response:
# {
#   "id": 1,
#   "original_url": "https://www.example.com/very/long/url",
#   "short_code": "abc123",
#   "short_url": "http://localhost:8000/abc123",
#   "clicks": 0,
#   ...
# }

# Access the short URL
curl -L http://localhost:8000/abc123
```

### Custom Short Codes

```bash
curl -X POST http://localhost:8000/api/urls/ \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://www.example.com",
    "custom_code": "mycode",
    "title": "My Custom Link"
  }'
```

## Verify Everything is Working

```bash
# Check all services are running
docker-compose ps

# Expected output:
# NAME                       STATUS
# urlshortener_postgres      Up (healthy)
# urlshortener_redis         Up (healthy)
# urlshortener_backend       Up
# urlshortener_celery_worker Up
# urlshortener_celery_beat   Up
# urlshortener_frontend      Up
# urlshortener_nginx         Up
```

## View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery_worker
```

## Common Issues

### Port Already in Use

If you get port conflicts, edit `docker-compose.yml` to change port mappings:

```yaml
frontend:
  ports:
    - "3001:3000"  # Change 3000 to 3001

backend:
  ports:
    - "8001:8000"  # Change 8000 to 8001
```

### Database Connection Error

```bash
# Restart PostgreSQL
docker-compose restart postgres

# If issue persists, recreate the database
docker-compose down -v
docker-compose up -d
```

### Frontend Build Errors

```bash
# Rebuild frontend
docker-compose up -d --build frontend

# Or manually install dependencies
docker-compose exec frontend npm install
```

## Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove all data (⚠️ destroys database)
docker-compose down -v
```

## Next Steps

1. **Explore the Admin Panel**: http://localhost:8000/admin/
2. **Check API Documentation**: http://localhost:8000/api/docs/
3. **Create More URLs**: Try custom codes, titles, and expiration dates
4. **View Analytics**: Go to Analytics tab to see statistics
5. **Generate QR Codes**: Each URL automatically gets a QR code

## Production Deployment

For production deployment, see [README.md](README.md) and [SETUP.md](SETUP.md).

Key changes needed:
- Set `DEBUG=False` in `.env`
- Use strong `SECRET_KEY` and database passwords
- Configure `DJANGO_ALLOWED_HOSTS`
- Set up SSL/TLS certificates
- Use proper domain names
- Configure external PostgreSQL if needed

## Support

- **Documentation**: See [README.md](README.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Detailed Setup**: See [SETUP.md](SETUP.md)

Happy URL shortening! 🚀
