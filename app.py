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
    page_icon="chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for attractive UI
st.markdown("""
    <style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border-left: 5px solid #fff;
    }
    
    /* Header styling */
    .header-style {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        margin-bottom: 30px;
    }
    
    /* Positive sentiment */
    .positive {
        color: #10b981;
        font-weight: bold;
        font-size: 16px;
    }
    
    /* Negative sentiment */
    .negative {
        color: #f59e0b;
        font-weight: bold;
        font-size: 16px;
    }
    
    /* Neutral sentiment */
    .neutral {
        color: #6366f1;
        font-weight: bold;
        font-size: 16px;
    }
    
    /* Section styling */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 20px 0 15px 0;
        font-weight: bold;
        font-size: 18px;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #fff;
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #fff;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Metric value */
    .metric-value {
        color: #667eea;
        font-size: 28px;
        font-weight: bold;
    }
    
    /* Metric label */
    .metric-label {
        color: #666;
        font-size: 14px;
        font-weight: 500;
    }
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
            status = "Good"
        elif sentiment.polarity < -0.1:
            category = "Negative"
            status = "Bad"
        else:
            category = "Neutral"
            status = "Neutral"
        
        return {
            'polarity': sentiment.polarity,
            'subjectivity': sentiment.subjectivity,
            'category': category,
            'status': status,
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
    st.markdown("""
    <div class="header-style">
        <h1 style="margin: 0; font-size: 42px;">SENTIMENT ANALYTICS PLATFORM</h1>
        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Extract Powerful Insights from Customer Feedback</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.markdown("<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px; text-align: center;'><h2 style='margin: 0;'>CONFIGURATION</h2></div>", unsafe_allow_html=True)
        
        st.markdown("")
        analysis_mode = st.radio(
            "Analysis Mode",
            ["Single Document", "Batch Analysis"],
            help="Choose your analysis mode"
        )
        
        industry = st.selectbox(
            "Select Industry",
            ["E-Commerce", "SaaS", "Hospitality", "Healthcare", "General"],
            help="Industry context for insights"
        )
        
        st.divider()
        st.markdown("<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 15px; border-radius: 10px; text-align: center;'><h3 style='margin: 0;'>UPLOAD FILE</h3></div>", unsafe_allow_html=True)
        st.markdown("")
        uploaded_file = st.file_uploader(
            "Choose a file (TXT or PDF)",
            type=['txt', 'pdf'],
            help="Upload customer reviews or feedback documents"
        )
    
    # Main content
    if uploaded_file is not None:
        st.markdown(f"""
        <div class="info-box">
            <strong>FILE UPLOADED:</strong> {uploaded_file.name}
        </div>
        """, unsafe_allow_html=True)
        
        # Process document
        processor = DocumentProcessor()
        text, error = processor.read_file(uploaded_file)
        
        if error:
            st.error(error)
            return
        
        if text:
            # Show text preview
            with st.expander("[PREVIEW] Document Preview", expanded=False):
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
                st.markdown("<div class='section-header'>[RESULTS] Sentiment Analysis Results</div>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Polarity Score</div>
                        <div class="metric-value">{analysis['polarity']:.2f}</div>
                        <small>Range: -1 to +1</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Subjectivity</div>
                        <div class="metric-value">{analysis['subjectivity']:.2f}</div>
                        <small>Range: 0 to 1</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">NPS Score</div>
                        <div class="metric-value">{analysis['nps_score']:.0f}</div>
                        <small>0-100 Scale</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    sentiment_color = "#10b981" if analysis['category'] == "Positive" else "#f59e0b" if analysis['category'] == "Negative" else "#6366f1"
                    st.markdown(f"""
                    <div class="metric-card" style="text-align: center;">
                        <div class="metric-label">Sentiment</div>
                        <div class="metric-value" style="color: {sentiment_color};">{analysis['status']}</div>
                        <small>{analysis['category']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detailed insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<div class='section-header'>[GAUGE] Polarity Gauge</div>", unsafe_allow_html=True)
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
                    st.markdown("<div class='section-header'>[EMOTION] Emotion Detected</div>", unsafe_allow_html=True)
                    emotion_data = pd.DataFrame({
                        'Emotion': [analysis['emotion']],
                        'Confidence': ['High']
                    })
                    st.dataframe(emotion_data, use_container_width=True)
                    st.text(f"Detected Emotion: **{analysis['emotion']}**")
                
                # Keyword extraction
                st.markdown("<div class='section-header'>[KEYWORDS] Top Keywords Found</div>", unsafe_allow_html=True)
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
                st.markdown(f"<div class='section-header'>[INDUSTRY] {industry} Industry Insights</div>", unsafe_allow_html=True)
                
                insights = get_industry_insights(analysis, text, industry)
                for insight in insights:
                    st.markdown(f"<div class='success-box'>✓ {insight}</div>", unsafe_allow_html=True)
                
                # Recommendations
                st.markdown("<div class='section-header'>[RECOMMENDATIONS] Action Items</div>", unsafe_allow_html=True)
                recommendations = get_recommendations(analysis, industry)
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")
                
                # Export options
                st.divider()
                st.markdown("<div class='section-header'>[EXPORT] Download Your Report</div>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("[CSV] Export as CSV"):
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
                    if st.button("[REPORT] Generate Report"):
                        st.success("Report generation coming in v2.1")
                
                # Save to history
                st.session_state.analysis_history.append({
                    'timestamp': datetime.now(),
                    'file': uploaded_file.name,
                    'sentiment': analysis['category'],
                    'polarity': analysis['polarity']
                })
    
    else:
        # Empty state with attractive welcome
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <h1 style="font-size: 48px; margin: 0;">Welcome!</h1>
            <p style="font-size: 18px; margin: 20px 0;">Customer Service Analytics Platform</p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px;">
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 15px; text-align: center;">
                <h3>Step 1</h3>
                <p>Upload a TXT or PDF file from the sidebar</p>
            </div>
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 15px; text-align: center;">
                <h3>Step 2</h3>
                <p>View comprehensive sentiment analysis</p>
            </div>
            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 25px; border-radius: 15px; text-align: center;">
                <h3>Step 3</h3>
                <p>Get industry-specific insights</p>
            </div>
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 25px; border-radius: 15px; text-align: center;">
                <h3>Step 4</h3>
                <p>Export your detailed reports</p>
            </div>
        </div>
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; margin-top: 30px; text-align: center;">
            <h2>Key Features</h2>
            <ul style="list-style: none; padding: 0; text-align: left; display: inline-block;">
                <li>✓ Advanced Sentiment Analysis</li>
                <li>✓ Emotion Detection (Happy/Sad/Angry/Neutral)</li>
                <li>✓ Keyword Extraction</li>
                <li>✓ Industry Insights</li>
                <li>✓ NPS Scoring</li>
                <li>✓ Export Reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

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
        insights.append("[URGENT] HIGH PRIORITY: Address customer concerns urgently to prevent escalation.")
    
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
