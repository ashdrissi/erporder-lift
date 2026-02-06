# ERPNext Elevator Extensions Deployment

This repository contains a Docker-based deployment setup for ERPNext with the custom `elevator_extensions` app.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Git
- At least 4GB RAM available

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashdrissi/erporder-lift.git
   cd erporder-lift/docker-deployment
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and set your passwords
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Create a new site**
   ```bash
   docker-compose exec backend bench new-site erpnext.localhost \
     --admin-password admin \
     --db-root-password admin \
     --install-app erpnext \
     --install-app elevator_extensions
   ```

5. **Access ERPNext**
   - URL: http://localhost:8080
   - Username: Administrator
   - Password: (what you set in step 4)

## 🔧 Coolify Deployment

### Method 1: Docker Compose (Recommended)

1. **In Coolify Dashboard:**
   - Create new resource → Docker Compose
   - Connect your GitHub repository
   - Set base directory: `docker-deployment`
   - Coolify will automatically detect `docker-compose.yml`

2. **Environment Variables:**
   Add these in Coolify:
   ```
   DB_PASSWORD=<secure-password>
   ADMIN_PASSWORD=<secure-password>
   SITE_NAME=<your-domain.com>
   ```

3. **Deploy:**
   - Click Deploy
   - Wait for all services to start
   - Run one-time site creation command

### Method 2: Dockerfile

1. **In Coolify:**
   - Create new resource → Dockerfile
   - Repository: `https://github.com/ashdrissi/erporder-lift`
   - Dockerfile location: `docker-deployment/Dockerfile`
   - Port: 8080

2. **Post-deployment:**
   Run site creation via Coolify console

## 📦 What's Included

- **ERPNext v15**: Latest stable version
- **Elevator Extensions**: Custom app for elevator/lift business
- **MariaDB**: Database
- **Redis**: Caching and queue management
- **Nginx**: Web server
- **Background Workers**: For async tasks

## 🛠️ Custom App: elevator_extensions

Features included:
- Portal for quotations (`/quotations`)
- Simplified desk interface
- Logistics management
- CRM and sales workflow
- French contract generators

## 📝 Common Commands

```bash
# View logs
docker-compose logs -f backend

# Access bench console
docker-compose exec backend bench console

# Run migrations
docker-compose exec backend bench migrate

# Restart services
docker-compose restart

# Stop all services
docker-compose down
```

## 🔒 Security Notes

- **Always change default passwords** in production
- Use strong DB_PASSWORD and ADMIN_PASSWORD
- Enable SSL/TLS in production (Coolify handles this)
- Regularly backup your database

## 🐛 Troubleshooting

### Site not accessible
```bash
docker-compose exec backend bench --site erpnext.localhost set-config developer_mode 0
docker-compose restart
```

### Database connection issues
```bash
docker-compose exec db mysql -uroot -padmin
# Check if database exists
SHOW DATABASES;
```

### Worker not processing jobs
```bash
docker-compose logs -f worker
docker-compose restart worker
```

## 📚 Documentation

- [ERPNext Docs](https://docs.erpnext.com)
- [Frappe Framework](https://frappeframework.com/docs)
- [Coolify Docs](https://coolify.io/docs)

## 🤝 Support

For issues specific to elevator_extensions, please open an issue on GitHub.

## 📄 License

This project uses ERPNext which is licensed under GPLv3.
