"""
Test suite for the Customer Service Analytics Platform
Run with: pytest tests.py -v
"""
import pytest
import pandas as pd
from textblob import TextBlob

class TestSentimentAnalysis:
    """Test sentiment analysis functionality"""
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        text = "This product is amazing! I love it."
        blob = TextBlob(text)
        assert blob.sentiment.polarity > 0
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        text = "This is terrible and useless."
        blob = TextBlob(text)
        assert blob.sentiment.polarity < 0
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment detection"""
        text = "The product comes in blue and red colors."
        blob = TextBlob(text)
        assert -0.2 < blob.sentiment.polarity < 0.2
    
    def test_empty_text(self):
        """Test handling of empty text"""
        text = ""
        blob = TextBlob(text)
        assert blob.sentiment.polarity == 0

class TestDataProcessing:
    """Test data processing functionality"""
    
    def test_text_cleaning(self):
        """Test text normalization"""
        from utils import TextProcessor
        processor = TextProcessor()
        dirty_text = "  HELLO   World!  "
        clean = processor.clean_text(dirty_text)
        assert clean == "hello   world!"
    
    def test_keyword_extraction(self):
        """Test keyword extraction"""
        from utils import TextProcessor
        processor = TextProcessor()
        text = "Python is great. Python programming is fun. I love Python."
        keywords = processor.extract_keywords(text, top_n=3)
        assert len(keywords) <= 3
        assert any(word[0] == 'python' for word in keywords)
    
    def test_text_chunking(self):
        """Test text chunking"""
        from utils import TextProcessor
        processor = TextProcessor()
        long_text = " ".join(["word"] * 100)
        chunks = processor.chunk_text(long_text, chunk_size=50)
        assert len(chunks) > 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])