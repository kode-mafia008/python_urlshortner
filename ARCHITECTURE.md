# System Architecture

## Overview

This URL shortener is built as a scalable, production-ready full-stack application using modern technologies and best practices.

## Technology Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - RESTful API
- **PostgreSQL 15** - Primary database
- **Redis 7** - Caching and message broker
- **Celery** - Distributed task queue
- **Celery Beat** - Periodic task scheduler
- **Gunicorn** - WSGI HTTP server

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **React Hook Form** - Form management
- **Recharts** - Data visualization
- **Lucide React** - Icon library

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and static file server

## System Components

### 1. Django Backend (`backend/`)

#### Models (`shortener/models.py`)
- **URL Model**: Stores URL mappings with analytics
  - Original URL, short code, custom code flag
  - Click counters (total and unique)
  - Metadata: title, description, expiration
  - QR code image reference
  
- **Click Model**: Individual click tracking
  - User agent parsing (device, browser, OS)
  - IP address and session tracking
  - Referrer and geolocation data
  - Timestamp for analytics

- **DailyAnalytics Model**: Aggregated statistics
  - Daily click counts per URL
  - Unique visitor counts
  - Used for trending and reporting

#### API Endpoints (`shortener/views.py`)
- `POST /api/urls/` - Create short URL
- `GET /api/urls/` - List URLs (paginated, searchable)
- `GET /api/urls/{id}/` - Get URL details
- `PATCH /api/urls/{id}/` - Update URL
- `DELETE /api/urls/{id}/` - Soft delete URL
- `GET /api/urls/{id}/stats/` - Detailed analytics
- `GET /api/urls/{id}/qrcode/` - Generate QR code
- `GET /api/urls/popular/` - Top URLs by clicks
- `GET /api/urls/recent/` - Recently created URLs
- `GET /{short_code}/` - Redirect to original URL

#### Background Tasks (`shortener/tasks.py`, `analytics/tasks.py`)
- **track_click_async**: Asynchronous click recording
  - Parses user agent
  - Identifies unique visitors
  - Updates counters atomically
  
- **generate_qr_code_async**: QR code generation
  - Creates QR code image
  - Saves to media storage
  
- **aggregate_analytics**: Daily aggregation
  - Runs hourly via Celery Beat
  - Summarizes click data
  
- **cleanup_old_analytics**: Data retention
  - Runs daily at 2 AM
  - Removes old click records
  
- **update_url_rankings**: Trending calculation
  - Runs every 30 minutes
  - Updates top URL cache

### 2. Next.js Frontend (`frontend/`)

#### Pages (`app/`)
- **layout.tsx**: Root layout with global styles
- **page.tsx**: Main application with tab navigation
- **globals.css**: Global CSS with Tailwind

#### Components (`components/`)
- **URLShortener**: Create new short URLs
  - Form validation with react-hook-form
  - Custom code input
  - QR code display
  - Copy-to-clipboard functionality
  
- **URLList**: Browse and manage URLs
  - Search and filtering
  - Pagination
  - Click statistics
  - Delete functionality
  
- **Dashboard**: Analytics overview
  - Total statistics cards
  - Top URLs ranking
  - Trend charts
  - Activity visualization

#### API Layer (`lib/api.ts`)
- Axios client configuration
- TypeScript interfaces for type safety
- Service methods for all API operations
- Error handling

### 3. Database Schema

```
┌─────────────────────┐
│       URL           │
├─────────────────────┤
│ id (PK)            │
│ original_url       │
│ short_code (UNIQUE)│
│ custom_code        │
│ title              │
│ description        │
│ clicks             │
│ unique_clicks      │
│ last_accessed      │
│ is_active          │
│ expires_at         │
│ created_at         │
│ updated_at         │
│ created_by_ip      │
│ qr_code            │
└─────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────┐
│      Click          │
├─────────────────────┤
│ id (PK)            │
│ url_id (FK)        │
│ ip_address         │
│ user_agent         │
│ referer            │
│ country            │
│ city               │
│ device_type        │
│ browser            │
│ os                 │
│ clicked_at         │
│ session_id         │
└─────────────────────┘
         │
         │ N:1 (aggregated)
         ▼
┌─────────────────────┐
│  DailyAnalytics     │
├─────────────────────┤
│ id (PK)            │
│ url_id (FK)        │
│ date               │
│ clicks             │
│ unique_visitors    │
└─────────────────────┘
```

### 4. Request Flow

#### Creating a Short URL
```
User → Frontend Form → POST /api/urls/
                           ↓
                    Django View (validates)
                           ↓
                    Database (save URL)
                           ↓
                    Celery Task (generate QR)
                           ↓
                    Response (short URL + details)
```

#### Accessing a Short URL
```
User → /{short_code}/ → RedirectView
                            ↓
                     Check Cache (Redis)
                            ↓
                     If miss → Database
                            ↓
                     Celery Task (track click)
                            ↓
                     HTTP 302 Redirect
```

#### Analytics Aggregation
```
Celery Beat (hourly) → aggregate_analytics task
                              ↓
                        Query Click records
                              ↓
                        Group by URL + Date
                              ↓
                        Update DailyAnalytics
```

## Scalability Features

### 1. Caching Strategy
- **URL Cache**: Short code → URL object (1 hour TTL)
- **QR Code Cache**: Generated QR codes (1 hour TTL)
- **Rankings Cache**: Top URLs (30 min TTL)

### 2. Database Optimization
- **Indexes**: short_code, created_at, clicks, session_id
- **Connection Pooling**: Reuse database connections
- **Async Operations**: Click tracking doesn't block redirects

### 3. Background Processing
- **Celery Workers**: Horizontal scaling
- **Task Queues**: Separate queues for different task types
- **Retry Logic**: Failed tasks automatically retried

### 4. Load Balancing
- **Nginx**: Distributes traffic
- **Multiple Workers**: Gunicorn with 4 workers
- **Celery Concurrency**: 4 concurrent tasks

## Security Measures

1. **Rate Limiting**: 10 requests/minute per IP
2. **Input Validation**: URL and custom code sanitization
3. **CORS Configuration**: Controlled cross-origin access
4. **SQL Injection Protection**: ORM-based queries
5. **Environment Variables**: Secure secret management
6. **CSRF Protection**: Django CSRF middleware

## Monitoring & Logging

- **Application Logs**: Django logging to stdout
- **Celery Logs**: Task execution tracking
- **Database Logs**: Query performance monitoring
- **Nginx Access Logs**: Request tracking

## Deployment Architecture

```
                    Internet
                       │
                       ▼
                   [Nginx:80]
                   /        \
                  /          \
           [Backend:8000]  [Frontend:3000]
                 │              │
                 ├──────────────┘
                 │
        ┌────────┼────────┐
        │        │        │
   [Postgres] [Redis] [Celery]
     :5432     :6379   Workers
```

## Performance Considerations

### Backend
- Database query optimization with select_related/prefetch_related
- Redis caching for frequently accessed data
- Async task processing for non-blocking operations
- Database connection pooling

### Frontend
- Next.js automatic code splitting
- Image optimization
- Static generation where possible
- Client-side caching with Axios

## Future Enhancements

1. **Authentication**: User accounts and API keys
2. **Link Analytics**: Geographic heatmaps, time-series graphs
3. **Custom Domains**: Branded short URLs
4. **Link Preview**: OG tag scraping
5. **Bulk Operations**: Create multiple URLs at once
6. **Webhooks**: Event notifications
7. **A/B Testing**: Multiple destination URLs
8. **Password Protection**: Private links
9. **Expiring Links**: Time-based expiration
10. **CDN Integration**: Global content delivery
