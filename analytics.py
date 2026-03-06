"""
Advanced Analytics Module
Provides enterprise-grade sentiment analysis and customer insights
"""
import logging
from typing import Dict, List
from textblob import TextBlob
from utils import TextProcessor
import json

logger = logging.getLogger(__name__)

class AdvancedAnalytics:
    """Enterprise analytics engine for customer service data"""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.analysis_cache = {}
    
    def comprehensive_analysis(self, text: str, industry: str = "General") -> Dict:
        """Perform comprehensive multi-layer analysis"""
        try:
            # Basic sentiment
            blob = TextBlob(text)
            sentiment = blob.sentiment
            
            # Text statistics
            stats = self.text_processor.get_text_stats(text)
            
            # Keywords
            keywords = self.text_processor.extract_keywords(text, top_n=15)
            
            # Customer segmentation
            segment = self._segment_customer(sentiment.polarity)
            
            # NPS calculation
            nps = self._calculate_nps(sentiment.polarity)
            
            # Industry insights
            insights = self._generate_insights(text, sentiment, industry)
            
            result = {
                'polarity': sentiment.polarity,
                'subjectivity': sentiment.subjectivity,
                'nps_score': nps,
                'customer_segment': segment,
                'text_stats': stats,
                'top_keywords': keywords,
                'insights': insights,
                'recommendation_priority': self._calculate_priority(sentiment.polarity)
            }
            
            return result
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise
    
    @staticmethod
    def _segment_customer(polarity: float) -> str:
        """Segment customer into NPS categories"""
        nps_score = int((polarity + 1) * 50)
        if nps_score >= 70:
            return "Promoter"
        elif nps_score >= 50:
            return "Passive"
        else:
            return "Detractor"
    
    @staticmethod
    def _calculate_nps(polarity: float) -> int:
        """Calculate NPS score"""
        return max(0, min(100, int((polarity + 1) * 50)))
    
    @staticmethod
    def _calculate_priority(polarity: float) -> str:
        """Determine action priority"""
        if polarity < -0.5:
            return "Critical"
        elif polarity < -0.1:
            return "High"
        elif polarity < 0.3:
            return "Medium"
        else:
            return "Low"
    
    def _generate_insights(self, text: str, sentiment, industry: str) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        if sentiment.polarity < -0.5:
            insights.append("URGENT: High-priority issue detected")
        
        if sentiment.subjectivity > 0.8:
            insights.append("Strong emotional content - indicates customer passion")
        
        if len(text) < 50:
            insights.append("Brief feedback - may lack context")
        
        if industry == "E-Commerce":
            if "shipping" in text.lower():
                insights.append("Logistics feedback acknowledged")
        
        return insights

# Singleton instance
analytics_engine = AdvancedAnalytics()