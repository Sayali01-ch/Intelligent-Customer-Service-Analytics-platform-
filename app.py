import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
import PyPDF2
import io
import logging
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Set page config
st.set_page_config(
    page_title="Customer Service Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .positive { color: #28a745; }
    .negative { color: #dc3545; }
    .neutral { color: #ffc107; }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

class SentimentAnalyzer:
    """Enterprise-grade sentiment analysis engine"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def analyze_sentiment(self, text):
        """Perform comprehensive sentiment analysis"""
        if not text or len(text.strip()) == 0:
            return None
        
        blob = TextBlob(text)
        sentiment = blob.sentiment
        
        # Emotion detection based on keywords
        emotion = self._detect_emotion(text.lower())
        
        # Categorize sentiment
        if sentiment.polarity > 0.1:
            category = "Positive"
            emoji = "😊"
        elif sentiment.polarity < -0.1:
            category = "Negative"
            emoji = "😞"
        else:
            category = "Neutral"
            emoji = "😐"
        
        return {
            'polarity': sentiment.polarity,
            'subjectivity': sentiment.subjectivity,
            'category': category,
            'emoji': emoji,
            'emotion': emotion,
            'nps_score': self._calculate_nps(sentiment.polarity)
        }
    
    def _detect_emotion(self, text):
        """Simple emotion detection"""
        emotions = {
            'happy': ['good', 'great', 'excellent', 'amazing', 'love', 'perfect', 'awesome'],
            'sad': ['bad', 'poor', 'terrible', 'awful', 'hate', 'worst'],
            'angry': ['angry', 'frustrated', 'disappointed', 'useless', 'waste'],
            'neutral': []
        }
        
        for emotion, keywords in emotions.items():
            if any(keyword in text for keyword in keywords):
                return emotion.capitalize()
        return "Neutral"
    
    def _calculate_nps(self, polarity):
        """Calculate Net Promoter Score (0-100)"""
        nps = int((polarity + 1) * 50)
        return max(0, min(100, nps))
    
    def extract_keywords(self, text, top_n=10):
        """Extract top keywords from text"""
        words = [word.lower() for word in text.split() 
                if word.lower() not in self.stop_words and len(word) > 3]
        word_freq = Counter(words)
        return word_freq.most_common(top_n)

class DocumentProcessor:
    """Handle document upload and processing"""
    
    @staticmethod
    def read_file(uploaded_file):
        """Extract text from various file formats"""
        try:
            if uploaded_file.type == "text/plain":
                text = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            else:
                return None, "Unsupported file type"
            
            return text, None
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            return None, f"Error reading file: {str(e)}"

def main():
    # Header
    st.title("🔍 Intelligent Customer Service Analytics Platform")
    st.markdown("*Enterprise-Grade Sentiment Analysis & Business Intelligence*")
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        analysis_mode = st.radio(
            "Select Analysis Mode",
            ["Single Document", "Batch Analysis"],
            help="Choose between analyzing one document or multiple documents"
        )
        
        industry = st.selectbox(
            "Select Industry",
            ["E-Commerce", "SaaS", "Hospitality", "Healthcare", "General"],
            help="Industry context for insights"
        )
        
        st.divider()
        st.header("📤 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file (TXT or PDF)",
            type=['txt', 'pdf'],
            help="Upload customer reviews or feedback"
        )
    
    # Main content
    if uploaded_file is not None:
        st.info(f"📁 File: {uploaded_file.name}")
        
        # Process document
        processor = DocumentProcessor()
        text, error = processor.read_file(uploaded_file)
        
        if error:
            st.error(error)
            return
        
        if text:
            # Show text preview
            with st.expander("📄 Document Preview", expanded=False):
                st.text_area(
                    "Text Content",
                    text[:1500] + "..." if len(text) > 1500 else text,
                    height=150,
                    disabled=True
                )
            
            # Perform analysis
            analyzer = SentimentAnalyzer()
            analysis = analyzer.analyze_sentiment(text)
            
            if analysis:
                # Display key metrics
                st.divider()
                st.subheader("📊 Sentiment Analysis Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Polarity Score",
                        f"{analysis['polarity']:.2f}",
                        help="Range: -1 (Negative) to +1 (Positive)"
                    )
                
                with col2:
                    st.metric(
                        "Subjectivity",
                        f"{analysis['subjectivity']:.2f}",
                        help="Range: 0 (Objective) to 1 (Subjective)"
                    )
                
                with col3:
                    nps_color = "🟢" if analysis['nps_score'] > 50 else "🟡" if analysis['nps_score'] > 0 else "🔴"
                    st.metric(
                        "NPS Score",
                        f"{analysis['nps_score']:.0f}",
                        help="Net Promoter Score (0-100)"
                    )
                
                with col4:
                    st.metric(
                        "Sentiment",
                        f"{analysis['emoji']} {analysis['category']}"
                    )
                
                # Detailed insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🎯 Sentiment Classification")
                    fig = go.Figure(data=[go.Indicator(
                        mode="gauge+number",
                        value=analysis['polarity'] * 100,
                        title={'text': "Polarity"},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [-100, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [-100, 0], 'color': "lightgray"},
                                {'range': [0, 100], 'color': "gray"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    )])
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("💭 Emotion Detection")
                    emotion_data = pd.DataFrame({
                        'Emotion': [analysis['emotion']],
                        'Confidence': ['High']
                    })
                    st.dataframe(emotion_data, use_container_width=True)
                    st.text(f"Detected Emotion: **{analysis['emotion']}**")
                
                # Keyword extraction
                st.subheader("🔑 Top Keywords")
                keywords = analyzer.extract_keywords(text)
                keywords_df = pd.DataFrame(keywords, columns=['Keyword', 'Frequency'])
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    fig = px.bar(keywords_df, x='Frequency', y='Keyword', orientation='h',
                                title="Most Frequent Keywords", color='Frequency',
                                color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.dataframe(keywords_df, use_container_width=True)
                
                # Industry-specific insights
                st.divider()
                st.subheader(f"🏢 {industry} Industry Insights")
                
                insights = get_industry_insights(analysis, text, industry)
                for insight in insights:
                    st.info(f"💡 {insight}")
                
                # Recommendations
                st.subheader("✅ Recommendations")
                recommendations = get_recommendations(analysis, industry)
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")
                
                # Export options
                st.divider()
                st.subheader("📥 Export Results")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📊 Export as CSV"):
                        export_df = pd.DataFrame({
                            'Metric': ['Polarity', 'Subjectivity', 'NPS Score', 'Sentiment', 'Emotion'],
                            'Value': [
                                f"{analysis['polarity']:.2f}",
                                f"{analysis['subjectivity']:.2f}",
                                f"{analysis['nps_score']:.0f}",
                                analysis['category'],
                                analysis['emotion']
                            ]
                        })
                        csv = export_df.to_csv(index=False)
                        st.download_button("Download CSV", csv, "analysis.csv", "text/csv")
                
                with col2:
                    if st.button("📋 Generate Report"):
                        st.success("Report generation coming in v2.1")
                
                # Save to history
                st.session_state.analysis_history.append({
                    'timestamp': datetime.now(),
                    'file': uploaded_file.name,
                    'sentiment': analysis['category'],
                    'polarity': analysis['polarity']
                })
    
    else:
        # Empty state
        st.markdown("""
        ### 👋 Welcome to Customer Service Analytics Platform
        
        **Get started:**
        1. Upload a document (TXT or PDF) from the sidebar
        2. View comprehensive sentiment analysis
        3. Get industry-specific insights
        4. Export your results
        
        ### 🎯 Key Features
        - 📊 Advanced sentiment analysis
        - 🎭 Emotion detection
        - 🔑 Keyword extraction
        - 💼 Industry insights
        - 📈 NPS scoring
        """)

def get_industry_insights(analysis, text, industry):
    """Generate industry-specific insights"""
    insights = []
    
    if industry == "E-Commerce":
        if analysis['polarity'] > 0.5:
            insights.append("Excellent customer satisfaction - prioritize maintaining this quality level.")
        elif analysis['polarity'] < -0.3:
            insights.append("Address product quality or shipping issues immediately.")
        
        if "product" in text.lower():
            insights.append("Focus on consistent product quality and accurate descriptions.")
        if "shipping" in text.lower() or "delivery" in text.lower():
            insights.append("Review logistics and delivery processes.")
    
    elif industry == "SaaS":
        if "feature" in text.lower():
            insights.append("Capture detailed feedback on feature requests for product roadmap.")
        if "bug" in text.lower() or "error" in text.lower():
            insights.append("Investigate reported bugs and improve error handling.")
        if analysis['polarity'] < 0:
            insights.append("Consider user experience improvements or onboarding enhancements.")
    
    elif industry == "Hospitality":
        if "staff" in text.lower() or "service" in text.lower():
            insights.append("Staff performance is a key satisfaction driver - invest in training.")
        if "cleanliness" in text.lower():
            insights.append("Maintain or improve facility cleanliness standards.")
        if "price" in text.lower() or "cost" in text.lower():
            insights.append("Review pricing strategy and value proposition.")
    
    elif industry == "Healthcare":
        if "doctor" in text.lower() or "physician" in text.lower():
            insights.append("Patient-doctor relationships are crucial - monitor care quality.")
        if "wait" in text.lower():
            insights.append("Reduce wait times to improve patient satisfaction.")
        if analysis['subjectivity'] > 0.7:
            insights.append("Strong emotional content indicates significant patient concerns.")
    
    if analysis['emotion'] == "Angry":
        insights.append("⚠️ HIGH PRIORITY: Address customer concerns urgently to prevent escalation.")
    
    if analysis['polarity'] > 0.7:
        insights.append("This is a promoter account - leverage for testimonials and referrals.")
    
    return insights if insights else ["No specific insights for this industry context."]

def get_recommendations(analysis, industry):
    """Generate actionable recommendations"""
    recommendations = []
    
    if analysis['polarity'] < -0.5:
        recommendations.append("Create immediate action plan to address critical issues")
        recommendations.append("Assign dedicated team member to resolve customer concerns")
        recommendations.append("Set up follow-up communication within 48 hours")
    
    if analysis['polarity'] > 0.5:
        recommendations.append("Share positive feedback with relevant teams")
        recommendations.append("Document best practices that led to satisfaction")
        recommendations.append("Consider case study or testimonial opportunity")
    
    if 0.2 < analysis['subjectivity'] < 0.8:
        recommendations.append("Customer has balanced opinion - gather more specific feedback")
    
    if industry == "E-Commerce":
        recommendations.append("Integrate feedback into product improvement cycle")
    
    if len(recommendations) == 0:
        recommendations.append("Continue current operations and monitor trends")
    
    return recommendations

if __name__ == "__main__":
    main()