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

## 🏗️ Tech Stack

**Backend:** Django 4.2, Django REST Framework, PostgreSQL, Redis, Celery, Celery Beat, Gunicorn  
**Frontend:** Next.js 14, TypeScript, TailwindCSS, React Hook Form, Recharts, Lucide React  
**Infrastructure:** Docker, Docker Compose, Nginx

## 📋 Prerequisites

- **Docker & Docker Compose** (required)
- Node.js 18+ (optional, for local development)
- Python 3.11+ (optional, for local development)

## 🚀 Quick Start

### Automated Setup (Recommended)

```bash
./bootstrap.sh
```

The interactive script will:
- ✅ Create `.env` file if missing
- ✅ Let you choose Development or Production mode
- ✅ Start all services (postgres, redis, backend, frontend, nginx, celery)
- ✅ Run migrations automatically

**Development Mode** - Hot-reload enabled for Django & Next.js  
**Production Mode** - Optimized builds with Gunicorn

### Manual Setup

```bash
# 1. Setup environment
cp .env.example .env

# 2. Start services
docker-compose -f docker-compose.dev.yml up -d --build  # Dev mode
# OR
docker-compose up -d --build  # Production mode

# 3. Run migrations
docker-compose exec backend python manage.py migrate

# 4. Create admin user
docker-compose exec backend python manage.py createsuperuser
```

### Access Points

- **Frontend**: http://localhost/
- **API**: http://localhost/api/
- **Admin**: http://localhost/admin/
- **API Docs**: http://localhost/api/docs/

## 💻 Local Development (Without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# In separate terminals:
celery -A config worker --loglevel=info
celery -A config beat --loglevel=info
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📚 API Overview

Full API documentation available at http://localhost/api/docs/

**Key Endpoints:**
- `POST /api/urls/` - Create short URL
- `GET /api/urls/` - List all URLs
- `GET /api/urls/{id}/` - URL details
- `GET /api/urls/{id}/stats/` - URL statistics
- `GET /{short_code}/` - Redirect to original URL
- `GET /api/analytics/dashboard/` - Dashboard metrics

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=localhost,yourdomain.com

# Database
POSTGRES_DB=urlshortener
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password

# URL Settings
BASE_URL=http://localhost
SHORT_CODE_LENGTH=6
```

See `.env.example` for all configuration options.

## 🐳 Common Commands

```bash
# View logs
docker-compose logs -f [service_name]

# Run Django commands
docker-compose exec backend python manage.py <command>

# Access database
docker-compose exec postgres psql -U postgres -d urlshortener

# Stop all services
docker-compose down
```

## 📊 Project Structure

```
.
├── backend/           # Django REST API
│   ├── config/        # Django settings
│   ├── shortener/     # URL shortening app
│   └── analytics/     # Analytics app
├── frontend/          # Next.js UI
│   ├── app/           # Next.js 14 app router
│   ├── components/    # React components
│   └── lib/           # Utilities
├── nginx/             # Nginx configuration
├── docs/              # Detailed documentation
│   ├── ARCHITECTURE.md
│   ├── QUICKSTART.md
│   ├── SETUP.md
│   └── TESTING.md
├── bootstrap.sh       # Setup script
├── docker-compose.yml
└── docker-compose.dev.yml
```

## 🔒 Key Features

- Rate limiting & input validation
- Redis caching for performance
- Celery for async tasks
- PostgreSQL with optimized indexing
- Comprehensive test coverage

## 🧪 Testing

```bash
# Backend (pytest)
cd backend
pytest --cov=. --cov-report=html

# Frontend (Jest)
cd frontend
npm test
```

See `docs/TESTING.md` for detailed testing documentation.

## 📦 Deployment

1. Update `.env` for production:
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure `DJANGO_ALLOWED_HOSTS`
   - Set up SSL certificates

2. Deploy:
   ```bash
   docker-compose up -d --build
   ```

See `docs/` folder for detailed guides.

## 📖 Documentation

Detailed documentation in the `docs/` folder:
- **ARCHITECTURE.md** - System architecture & design
- **QUICKSTART.md** - Quick setup guide
- **SETUP.md** - Detailed setup instructions
- **TESTING.md** - Testing strategy & guides
- **QUICK_REFERENCE.md** - Command reference

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please create an issue in the repository.

---

Built with ❤️ using Django, PostgreSQL, Next.js, and TypeScript
