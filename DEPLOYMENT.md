# Deployment Guide

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
