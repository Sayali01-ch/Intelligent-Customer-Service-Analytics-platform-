"""
Database models for the Customer Service Analytics Platform
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    analyses = relationship("Analysis", back_populates="user")

class Analysis(Base):
    """Analysis results model"""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_content = Column(Text)
    polarity = Column(Float, nullable=False)
    subjectivity = Column(Float, nullable=False)
    sentiment_category = Column(String, nullable=False)
    emotion = Column(String)
    nps_score = Column(Float)
    industry = Column(String, default="General")
    keywords = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="analyses")
    insights = relationship("Insight", back_populates="analysis")

class Insight(Base):
    """Analysis insights model"""
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    insight_type = Column(String, nullable=False)  # 'industry', 'recommendation', etc.
    content = Column(Text, nullable=False)
    priority = Column(String, default="medium")  # 'low', 'medium', 'high', 'urgent'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    analysis = relationship("Analysis", back_populates="insights")