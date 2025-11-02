# Hostname Setup for Backend and Frontend

This guide will help you set up custom hostnames so you can access:
- **http://backend** (equivalent to http://localhost:8000)
- **http://frontend** (equivalent to http://localhost:3000)

## Quick Setup

### 1. Edit Your Hosts File

On macOS/Linux, you need to edit `/etc/hosts`:

```bash
sudo nano /etc/hosts
```

### 2. Add These Lines

Add the following lines at the end of the file:

```
127.0.0.1   backend
127.0.0.1   frontend
```

Your `/etc/hosts` file should look something like this:

```
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1       localhost
255.255.255.255 broadcasthost
::1             localhost

# URL Shortener custom hostnames
127.0.0.1   backend
127.0.0.1   frontend
```

### 3. Save and Exit

- Press `Ctrl+O` to save
- Press `Enter` to confirm
- Press `Ctrl+X` to exit

### 4. Restart Nginx

```bash
docker-compose restart nginx
```

### 5. Flush DNS Cache (Optional but Recommended)

```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

## Testing

After setup, you can access:

1. **Backend (Django API)**:
   - http://backend/api/
   - http://backend/admin/
   - http://backend/api/docs/
   - Direct access to all Django endpoints

2. **Frontend (Next.js)**:
   - http://frontend/
   - React application interface

3. **Localhost (Combined - still works)**:
   - http://localhost/
   - http://localhost/api/
   - http://localhost/admin/

## How It Works

```
┌─────────────────────────────────────┐
│  Your Browser                       │
├─────────────────────────────────────┤
│  http://backend                     │
│  http://frontend                    │
│  http://localhost                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  /etc/hosts                          │
│  127.0.0.1   backend                 │
│  127.0.0.1   frontend                │
└──────────────┬───────────────────────┘
               │
               ▼ (Port 80)
┌──────────────────────────────────────┐
│  Nginx (urlshortener_nginx)          │
│                                       │
│  server_name backend    → backend:8000│
│  server_name frontend   → frontend:3000│
│  server_name localhost  → combined    │
└──────────────┬───────────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌─────────────┐  ┌──────────────┐
│  Backend    │  │  Frontend    │
│  :8000      │  │  :3000       │
└─────────────┘  └──────────────┘
```

## URLs Comparison

| Old Access | New Access | What It Shows |
|------------|-----------|---------------|
| http://localhost:8000/api/ | http://backend/api/ | Django API |
| http://localhost:8000/admin/ | http://backend/admin/ | Django Admin |
| http://localhost:8000/api/docs/ | http://backend/api/docs/ | API Documentation |
| http://localhost:3000 | http://frontend/ | React Frontend |
| http://localhost/ | http://localhost/ | Combined (unchanged) |

## Benefits

✅ Cleaner URLs (no port numbers)  
✅ Service-specific hostnames  
✅ More production-like setup  
✅ Easier to remember  
✅ Better separation of concerns  

## Troubleshooting

### "Cannot connect" or "Site not found"

1. Check if hosts file is correctly edited:
   ```bash
   cat /etc/hosts | grep -E 'backend|frontend'
   ```

2. Ensure Nginx is running:
   ```bash
   docker-compose ps nginx
   ```

3. Restart Nginx:
   ```bash
   docker-compose restart nginx
   ```

4. Flush DNS cache again

### Still using port numbers?

Make sure you're accessing through port 80 (default HTTP):
- ✅ http://backend (correct)
- ❌ http://backend:8000 (bypasses Nginx)

## Removing the Setup

To remove custom hostnames:

1. Edit hosts file:
   ```bash
   sudo nano /etc/hosts
   ```

2. Remove or comment out these lines:
   ```
   # 127.0.0.1   backend
   # 127.0.0.1   frontend
   ```

3. Flush DNS cache

## Production Deployment

For production with a real domain:

Instead of editing `/etc/hosts`, you would:
1. Purchase a domain (e.g., `yourapp.com`)
2. Create DNS A records:
   - `api.yourapp.com` → Your server IP
   - `app.yourapp.com` → Your server IP
3. Update Nginx `server_name` directives
4. Set up SSL/TLS certificates
