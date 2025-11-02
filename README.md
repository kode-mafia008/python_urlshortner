# URL Shortener - Full Stack Application

A modern, scalable URL shortening service built with Django, PostgreSQL, Next.js, TypeScript, and TailwindCSS. Features real-time analytics, QR code generation, and background task processing with Celery.

## 🚀 Features

- **URL Shortening**: Create short, memorable links from long URLs
- **Custom Short Codes**: Optional custom short codes for branded links
- **Analytics Dashboard**: Track clicks, unique visitors, and engagement metrics
- **QR Code Generation**: Automatic QR code creation for each short URL
- **Real-time Tracking**: Click tracking with device, browser, and location data
- **Background Tasks**: Asynchronous processing with Celery and Redis
- **Scheduled Jobs**: Automated analytics aggregation and cleanup
- **RESTful API**: Well-documented API with Swagger/ReDoc
- **Responsive UI**: Modern, mobile-friendly interface
- **Rate Limiting**: Protection against abuse
- **Caching**: Redis-powered caching for optimal performance

## 🏗️ Architecture

### Backend
- **Django 4.2**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Primary database
- **Redis**: Caching and Celery broker
- **Celery**: Asynchronous task processing
- **Celery Beat**: Scheduled task execution
- **Gunicorn**: WSGI HTTP server

### Frontend
- **Next.js 14**: React framework
- **TypeScript**: Type-safe development
- **TailwindCSS**: Utility-first styling
- **Axios**: HTTP client
- **React Hook Form**: Form validation
- **Recharts**: Data visualization
- **Lucide React**: Icons

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and load balancer

## 📋 Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
cd python_urlshortner
```

### 2. Configure Environment

Copy the example environment file and update as needed:

```bash
cp .env.example .env
```

Update the following variables in `.env`:
- `SECRET_KEY`: Generate a secure secret key
- `POSTGRES_PASSWORD`: Set a strong database password
- Database credentials if using external PostgreSQL

### 3. Start with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

This will start:
- **PostgreSQL** on port 5432
- **Redis** on port 6379
- **Django backend** on port 8000
- **Celery worker** (background)
- **Celery beat** (scheduler)
- **Next.js frontend** on port 3000
- **Nginx** on port 80

### 4. Run Database Migrations

```bash
docker-compose exec backend python manage.py migrate
```

### 5. Create Admin User

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/

## 💻 Local Development

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Start Celery Worker (for background tasks)

```bash
cd backend
celery -A config worker --loglevel=info
```

### Start Celery Beat (for scheduled tasks)

```bash
cd backend
celery -A config beat --loglevel=info
```

## 📚 API Documentation

### Create Short URL

```http
POST /api/urls/
Content-Type: application/json

{
  "original_url": "https://example.com/very-long-url",
  "custom_code": "mycode",  // Optional
  "title": "My Website",     // Optional
  "description": "...",      // Optional
  "expires_at": "2024-12-31T23:59:59Z"  // Optional
}
```

### Get URL Details

```http
GET /api/urls/{id}/
```

### Get URL Statistics

```http
GET /api/urls/{id}/stats/
```

### List All URLs

```http
GET /api/urls/?page=1&search=query&order_by=-clicks
```

### Access Short URL

```http
GET /{short_code}/
```

### Get Dashboard Stats

```http
GET /api/analytics/dashboard/
```

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=yourdomain.com

# Database
POSTGRES_DB=urlshortener
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# URL Shortener
BASE_URL=https://yourdomain.com
SHORT_CODE_LENGTH=6
ENABLE_CUSTOM_CODES=True

# Analytics
ANALYTICS_RETENTION_DAYS=90

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=10
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend

# Run Django commands
docker-compose exec backend python manage.py <command>

# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d urlshortener

# Access Redis CLI
docker-compose exec redis redis-cli
```

## 📊 Database Schema

### URL Model
- `id`: Primary key
- `original_url`: The long URL
- `short_code`: Unique short identifier
- `custom_code`: Boolean flag for custom codes
- `title`, `description`: Optional metadata
- `clicks`, `unique_clicks`: Analytics counters
- `is_active`, `expires_at`: Status fields
- `created_at`, `updated_at`: Timestamps

### Click Model
- Tracks individual clicks with:
  - IP address
  - User agent, device type, browser, OS
  - Referrer URL
  - Geolocation (country, city)
  - Session ID for unique visitor tracking
  - Timestamp

### DailyAnalytics Model
- Aggregated daily statistics per URL
- Clicks and unique visitors per day
- Used for trend analysis

## 🔒 Security Features

- **Rate Limiting**: Prevents abuse
- **Input Validation**: URL and custom code validation
- **CORS Configuration**: Controlled cross-origin access
- **Database Connection Pooling**: Efficient resource usage
- **Environment-based Configuration**: Secure secret management

## 📈 Performance Optimizations

- **Redis Caching**: Frequently accessed URLs cached
- **Database Indexing**: Optimized queries on short_code, created_at
- **Celery Background Tasks**: Async click tracking
- **Connection Pooling**: Reuse database connections
- **Static File Serving**: Nginx for efficient asset delivery

## 🧪 Testing

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

## 📦 Production Deployment

### Using Docker Compose

1. Update `.env` with production values
2. Set `DEBUG=False`
3. Configure proper `DJANGO_ALLOWED_HOSTS`
4. Use strong `SECRET_KEY` and database passwords
5. Set up SSL/TLS with Let's Encrypt
6. Configure Nginx for HTTPS

```bash
docker-compose -f docker-compose.yml up -d
```

### Manual Deployment

Refer to Django and Next.js deployment guides for platforms like:
- AWS (EC2, ECS, Elastic Beanstalk)
- Google Cloud Platform
- Heroku
- DigitalOcean
- Vercel (Frontend)

## 🛠️ Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Celery Not Processing Tasks

```bash
# Check Celery worker logs
docker-compose logs celery_worker

# Restart Celery worker
docker-compose restart celery_worker
```

### Frontend Build Errors

```bash
# Clear Next.js cache
rm -rf frontend/.next

# Rebuild
docker-compose up --build frontend
```

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please create an issue in the repository.

---

Built with ❤️ using Django, PostgreSQL, Next.js, and TypeScript
