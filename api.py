"""
FastAPI backend for Customer Service Analytics Platform
"""
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import json
import logging

from database import get_db, create_tables
from models import User, Analysis, Insight
from utils import TextProcessor
from analytics import AdvancedAnalytics
from auth import (
    authenticate_user, create_access_token, get_current_user,
    get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Customer Service Analytics API",
    description="Enterprise-grade customer service analytics platform",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8501"],  # React dev server & Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
@app.on_event("startup")
async def startup_event():
    create_tables()
    logger.info("Database tables created/verified")

# Authentication endpoints
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
async def register_user(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(None),
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully", "user_id": db_user.id}

# Analysis endpoints
@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    industry: str = Form("General"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze uploaded document"""
    try:
        # Read file content
        content = await file.read()
        text = content.decode("utf-8")

        # Perform analysis
        analyzer = AdvancedAnalytics()
        result = analyzer.comprehensive_analysis(text, industry)

        # Save to database
        keywords_json = json.dumps(result['top_keywords'])

        db_analysis = Analysis(
            user_id=current_user.id,
            filename=file.filename,
            file_content=text[:10000],  # Store first 10k chars
            polarity=result['polarity'],
            subjectivity=result['subjectivity'],
            sentiment_category=result['customer_segment'],
            emotion=result.get('emotion', 'Neutral'),
            nps_score=result['nps_score'],
            industry=industry,
            keywords=keywords_json
        )

        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)

        # Save insights
        for insight in result['insights']:
            db_insight = Insight(
                analysis_id=db_analysis.id,
                insight_type="industry",
                content=insight,
                priority=result['recommendation_priority']
            )
            db.add(db_insight)

        db.commit()

        return {
            "analysis_id": db_analysis.id,
            "results": result,
            "message": "Analysis completed successfully"
        }

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/analyses")
async def get_user_analyses(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's analysis history"""
    analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id)\
        .order_by(Analysis.created_at.desc())\
        .offset(skip).limit(limit).all()

    return [
        {
            "id": analysis.id,
            "filename": analysis.filename,
            "polarity": analysis.polarity,
            "sentiment_category": analysis.sentiment_category,
            "industry": analysis.industry,
            "created_at": analysis.created_at
        }
        for analysis in analyses
    ]

@app.get("/analysis/{analysis_id}")
async def get_analysis_details(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed analysis results"""
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    insights = db.query(Insight).filter(Insight.analysis_id == analysis_id).all()

    return {
        "id": analysis.id,
        "filename": analysis.filename,
        "polarity": analysis.polarity,
        "subjectivity": analysis.subjectivity,
        "sentiment_category": analysis.sentiment_category,
        "emotion": analysis.emotion,
        "nps_score": analysis.nps_score,
        "industry": analysis.industry,
        "keywords": json.loads(analysis.keywords),
        "insights": [{"content": i.content, "priority": i.priority} for i in insights],
        "created_at": analysis.created_at
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}