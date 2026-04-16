# 🚀 Deployment Guide - Intelligent Customer Service Analytics Platform

This guide covers deploying the platform to various environments: local development, Docker, cloud platforms, and production servers.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Platforms](#cloud-platforms)
4. [Production Recommendations](#production-recommendations)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis (optional)
- Git

### Step-by-Step Setup

#### 1. Clone Repository
```bash
git clone https://github.com/Sayali01-ch/Intelligent-Customer-Service-Analytics-platform-.git
cd Intelligent-Customer-Service-Analytics-platform-
```

#### 2. Setup Backend

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

#### 3. Setup Database

```bash
# Create PostgreSQL database
createdb customer_analytics

# Create tables
python -c "from database import create_tables; create_tables()"
```

#### 4. Start Backend Server

```bash
# Run the API server
python run_api.py
```

Backend will be available at: `http://localhost:8000`

#### 5. Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be available at: `http://localhost:3000`

---

## Docker Deployment

### Quick Start (Recommended)

```bash
# Clone repository
git clone https://github.com/Sayali01-ch/Intelligent-Customer-Service-Analytics-platform-.git
cd Intelligent-Customer-Service-Analytics-platform-

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### Access URLs
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Streamlit**: http://localhost:8501

---

## Cloud Platforms

### AWS Deployment

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Create ECR repository
aws ecr create-repository --repository-name analytics-api

# Deploy using ECS, RDS, and ElastiCache
# See AWS console for detailed setup
```

### Google Cloud Platform

```bash
# Deploy to Cloud Run
gcloud run deploy analytics-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku Deployment

```bash
# Install Heroku CLI and login
brew tap heroku/brew && brew install heroku
heroku login

# Create app
heroku create analytics-platform

# Add databases
heroku addons:create heroku-postgresql:standard-0
heroku addons:create heroku-redis:premium-0

# Deploy
git push heroku main
```

### DigitalOcean Deployment

```bash
# Create Droplet with Docker
# SSH into droplet
ssh root@your_droplet_ip

# Install Docker and start services
docker-compose up -d
```

---

## Production Recommendations

### 1. Environment Configuration

```env
DEBUG=False
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://user:password@prod-db:5432/customer_analytics
REDIS_URL=redis://:password@prod-redis:6379/0
SECRET_KEY=<VERY_SECURE_RANDOM_KEY>
CORS_ORIGINS=["https://yourdomain.com"]
```

### 2. Security Hardening

- Update all dependencies
- Use HTTPS/SSL
- Configure security headers
- Enable CORS with specific origins only
- Use environment variables for secrets

### 3. Reverse Proxy Setup (Nginx)

```nginx
upstream analytics_api {
    server api:8000;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location /api {
        proxy_pass http://analytics_api;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
```

### 4. Database Backups

```bash
# Daily backup script
pg_dump customer_analytics > backup_$(date +%Y%m%d).sql
gzip backup_$(date +%Y%m%d).sql

# Keep only last 30 days
find . -name "backup_*.sql.gz" -mtime +30 -delete
```

### 5. Monitoring & Logging

- Setup uptime monitoring
- Configure error tracking (Sentry)
- Enable structured logging
- Use APM tools (New Relic, DataDog)

---

## Monitoring & Maintenance

### Health Checks

```bash
# API health check
curl http://localhost:8000/health

# Database connectivity
psql -h localhost -U user customer_analytics -c "SELECT 1"

# Redis connectivity
redis-cli ping
```

### Logs

```bash
# View Docker logs
docker-compose logs -f api

# Save logs
docker-compose logs api > api.log
```

---

## Troubleshooting

### Port Conflicts

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database Connection Issues

```bash
# Test connection
psql -U user -h localhost -d customer_analytics -c "SELECT 1"

# Reset database
dropdb customer_analytics
createdb customer_analytics
python -c "from database import create_tables; create_tables()"
```

### Docker Issues

```bash
# Clean up
docker-compose down -v

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose up -d
```

---

## Cost Optimization

| Platform | Estimated Cost |
|----------|----------------|
| AWS | $50-100/month |
| GCP | $50-100/month |
| Heroku | $100-300/month |
| DigitalOcean | $25-100/month |
| Self-hosted | $10-50/month |

---

**Last Updated:** April 2026 | **Version:** 2.0.0# Deployment Guide

## Local Development

### Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

## Docker Deployment

### Build
```bash
docker build -t customer-analytics:latest .
```

### Run
```bash
docker run -p 8501:8501 customer-analytics:latest
```

### Docker Compose
```bash
docker-compose up -d
```

## Streamlit Cloud

1. Push code to GitHub
2. Go to Streamlit Cloud
3. Create new app
4. Select repository and branch
5. Set `app.py` as main file

## AWS Deployment

### ECS
```bash
aws ecr create-repository --repository-name customer-analytics
docker tag customer-analytics:latest \
  <account>.dkr.ecr.<region>.amazonaws.com/customer-analytics:latest
aws ecr push <account>.dkr.ecr.<region>.amazonaws.com/customer-analytics:latest
```

### EC2
```bash
ssh -i key.pem ec2-user@instance-ip
sudo yum install python3 python3-pip
git clone <repo>
cd Intelligent-Customer-Service-Analytics-platform-
pip install -r requirements.txt
nohup streamlit run app.py &
```

## Heroku

```bash
heroku login
heroku create customer-analytics-app
git push heroku main
```

## Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure .env with production values
- [ ] Set up monitoring and logging
- [ ] Configure SSL/TLS
- [ ] Set up automated backups
- [ ] Configure rate limiting
- [ ] Add authentication if needed
- [ ] Monitor application performance
- [ ] Set up CI/CD pipeline
- [ ] Document API endpoints
