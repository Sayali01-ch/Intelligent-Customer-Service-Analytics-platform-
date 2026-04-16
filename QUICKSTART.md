# ⚡ Quick Start Guide

Get the Intelligent Customer Service Analytics Platform running in 5 minutes!

## 🚀 5-Minute Setup (Docker)

### Prerequisites
- Docker installed ([Download](https://www.docker.com/products/docker-desktop))
- Git installed ([Download](https://git-scm.com/)) 

### Steps

```bash
# 1. Clone repository
git clone https://github.com/Sayali01-ch/Intelligent-Customer-Service-Analytics-platform-.git
cd Intelligent-Customer-Service-Analytics-platform-

# 2. Start all services
docker-compose up -d

# 3. Wait 30 seconds for services to start
sleep 30

# 4. Open in browser
# Frontend:  http://localhost:3000
# API:       http://localhost:8000
# Docs:      http://localhost:8000/docs
```

That's it! 🎉

---

## 📝 First-Time Usage

### Create Account
1. Go to http://localhost:3000
2. Click "Create a new account"
3. Enter:
   - **Email**: your@email.com
   - **Username**: your_username
   - **Password**: secure_password
   - **Full Name**: Your Name
4. Click "Create account"

### Login
1. Click "Login"
2. Enter username and password
3. Click "Sign in"

### Upload & Analyze
1. Click "New Analysis"
2. **Select file**: Choose a TXT or PDF file
3. **Choose industry**: E-Commerce, SaaS, Hospitality, Healthcare, or General
4. Click "Analyze Document"
5. Wait 5-10 seconds for results

### View Results
- **Sentiment Score**: -1 (negative) to +1 (positive)
- **NPS Score**: 0-100 scale
- **Emotion**: Happy, Sad, Angry, or Neutral
- **Keywords**: Top words from the text
- **Insights**: Industry-specific recommendations

### View History
1. Click "History"
2. Browse previous analyses
3. Click on any analysis for details
4. Export results if needed

---

## 🛠️ Local Development (Manual Setup)

### Prerequisites
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ ([Download](https://nodejs.org/))
- PostgreSQL 15+ ([Download](https://www.postgresql.org/download/))

### Backend Setup (Terminal 1)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb customer_analytics
python -c "from database import create_tables; create_tables()"

# Start API
python run_api.py
```

Backend runs on: **http://localhost:8000**

### Frontend Setup (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on: **http://localhost:3000**

### Legacy Streamlit (Terminal 3, Optional)

```bash
streamlit run app.py
```

Streamlit runs on: **http://localhost:8501**

---

## 🎯 Common Tasks

### Upload a Customer Review
1. Go to "New Analysis"
2. Paste review text or upload file:

   **Example:**
   ```
   Amazing product! Fast shipping and great customer service.
   The quality is excellent and price is fair. Would definitely
   recommend to everyone. 5 stars!
   ```

3. Select industry
4. Click "Analyze"

### View Sentiment Results
```
Polarity:     0.85 (Very positive)
Subjectivity: 0.65 (Somewhat subjective)
Emotion:      Happy
NPS Score:    93 (Promoter)
```

### Export Data
1. Go to "History"
2. Click on any analysis
3. Click "Export to CSV"
4. File downloads automatically

### Stop Services

```bash
# Docker
docker-compose down

# Local Development
# Press Ctrl+C in each terminal
```

---

## 🆘 Troubleshooting

### "Port 3000 already in use"
```bash
# Kill process
lsof -ti:3000 | xargs kill -9
# Then start again
```

### "Connection refused" on API
```bash
# Check if API is running
curl http://localhost:8000/health

# If not, restart
python run_api.py
```

### "Database connection error"
```bash
# Check PostgreSQL is running
psql -U postgres -l

# Create database
createdb customer_analytics

# Initialize tables
python -c "from database import create_tables; create_tables()"
```

### "npm install fails"
```bash
# Clear npm cache
npm cache clean --force

# Try again
npm install
```

---

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [FEATURES.md](FEATURES.md) for all capabilities
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- View [API Docs](http://localhost:8000/docs) for API reference

---

## 🐛 Report Issues

Found a bug? Have suggestions? 

- **GitHub Issue**: [Create Issue](https://github.com/Sayali01-ch/Intelligent-Customer-Service-Analytics-platform-/issues)
- **Email**: support@example.com
- **Discussions**: [GitHub Discussions](https://github.com/Sayali01-ch/Intelligent-Customer-Service-Analytics-platform-/discussions)

---

## 💡 Tips & Tricks

### Better Analysis Results
- Use clear, natural language
- Include specific details
- Use standard grammar
- Avoid abbreviations

### Performance Tips
- Analyze one document at a time
- Keep files under 10MB
- Use Chrome browser for best experience
- Clear browser cache if issues occur

### API Tips
- Visit `/docs` for interactive testing
- All endpoints require authentication token
- Rate limited to 100 requests/minute
- Response time < 200ms typical

---

**Need help?** Check [README.md](README.md) or open an issue on GitHub!

**Last Updated:** April 2026 | **Version:** 2.0.0