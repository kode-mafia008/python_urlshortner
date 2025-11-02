# Quick Reference Guide

## 🚀 Starting the Application

### Using the Setup Script (Recommended)

```bash
./entryPoint.sh
```

**Menu Options:**
- **1** - 🔥 Development Mode (Hot-Reload)
- **2** - 🚀 Production Mode  
- **3** - 🛑 Stop All Services
- **4** - 🚪 Exit

## 🔥 Development Mode vs 🚀 Production Mode

| Feature | Development | Production |
|---------|------------|------------|
| **Hot Reload** | ✅ Yes | ❌ No |
| **Auto Restart** | ✅ Yes | ❌ No |
| **Build Time** | Fast | Slower |
| **Performance** | Good | Optimized |
| **Server** | Django Dev Server | Gunicorn |
| **Frontend** | Next.js Dev | Next.js Build |
| **Use Case** | Coding & Testing | Deployment |

## 📝 Common Commands

### Development Mode

```bash
# Start
./entryPoint.sh  # Select option 1

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# View specific service logs
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f frontend

# Execute Django commands
docker-compose -f docker-compose.dev.yml exec backend python manage.py <command>

# Stop
docker-compose -f docker-compose.dev.yml down
```

### Production Mode

```bash
# Start
./entryPoint.sh  # Select option 2

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute Django commands
docker-compose exec backend python manage.py <command>

# Stop
docker-compose down
```

## 🔄 Making Code Changes

### In Development Mode (Hot-Reload)

**Backend (Django):**
1. Edit any `.py` file in `backend/`
2. Save the file
3. ✅ Changes auto-reload instantly
4. Refresh browser

**Frontend (Next.js):**
1. Edit any `.tsx`, `.ts`, or `.css` file in `frontend/`
2. Save the file
3. ✅ Browser auto-refreshes (Fast Refresh)

**No restarts needed!** 🎉

### In Production Mode

Changes require rebuild:
```bash
docker-compose down
docker-compose up -d --build
```

## 🗄️ Database Operations

```bash
# Development Mode
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate
docker-compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser
docker-compose -f docker-compose.dev.yml exec backend python manage.py makemigrations

# Production Mode
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py makemigrations
```

## 🐛 Debugging

### View Logs

```bash
# All services (Development)
docker-compose -f docker-compose.dev.yml logs -f

# All services (Production)
docker-compose logs -f

# Specific service
docker-compose logs -f <service_name>
# Examples: backend, frontend, celery_worker, postgres, redis
```

### Check Running Containers

```bash
docker ps
```

### Check Container Health

```bash
# Development
docker-compose -f docker-compose.dev.yml ps

# Production
docker-compose ps
```

### Access Container Shell

```bash
# Backend (Development)
docker-compose -f docker-compose.dev.yml exec backend bash

# Backend (Production)
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh
```

### Django Shell

```bash
# Development
docker-compose -f docker-compose.dev.yml exec backend python manage.py shell

# Production
docker-compose exec backend python manage.py shell
```

## 🔧 Troubleshooting

### "Port already in use"

```bash
# Stop all containers
docker-compose -f docker-compose.dev.yml down
docker-compose down

# Check what's using the port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
lsof -i :80    # Nginx
```

### "Changes not reflecting"

**Development Mode:**
- Check if containers are running: `docker ps`
- Check logs: `docker-compose -f docker-compose.dev.yml logs -f`
- Ensure you're using `docker-compose.dev.yml`

**Production Mode:**
- Rebuild: `docker-compose up -d --build`

### "Cannot connect to database"

```bash
# Check PostgreSQL health
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Clean Start

```bash
# Stop everything
docker-compose -f docker-compose.dev.yml down
docker-compose down

# Remove volumes (⚠️ deletes database!)
docker-compose down -v

# Start fresh
./entryPoint.sh
```

## 📦 Package Management

### Backend (Python)

```bash
# Add new package
echo "package-name==version" >> backend/requirements.txt

# Development Mode
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d --build

# Production Mode
docker-compose down
docker-compose up -d --build
```

### Frontend (Node.js)

```bash
# Add new package
cd frontend
npm install package-name

# Update docker-compose
# In Development Mode - auto-detected via volume mount
# In Production Mode - requires rebuild
```

## 🌐 URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost/ |
| Backend API | http://localhost/api/ |
| Admin Panel | http://localhost/admin/ |
| API Documentation | http://localhost/api/docs/ |
| Alternative API Docs | http://localhost/api/redoc/ |
| Backend Direct | http://backend/ (requires `/etc/hosts` setup) |
| Frontend Direct | http://frontend/ (requires `/etc/hosts` setup) |

## 💾 Data Persistence

Data is persisted in Docker volumes:
- **postgres_data** - PostgreSQL database
- **redis_data** - Redis cache
- **static_volume** - Django static files
- **media_volume** - Uploaded files

To backup:
```bash
docker run --rm -v postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres_backup.tar.gz /data
```

## 🎯 Best Practices

1. **Always use Development Mode when coding**
   - Faster feedback loop
   - Auto-reload saves time
   - Better debugging experience

2. **Test in Production Mode before deploying**
   - Catches build issues
   - Validates optimizations
   - Tests production configuration

3. **Commit your `.env` template, not the actual `.env`**
   - Keep secrets secret
   - Use `.env.example` for documentation

4. **Use git branches for features**
   - Hot-reload makes branch switching smooth
   - No need to rebuild for small changes

## 📞 Need Help?

- Check logs: `docker-compose logs -f`
- Read [README.md](README.md) for detailed info
- See [SETUP.md](SETUP.md) for installation guide
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
