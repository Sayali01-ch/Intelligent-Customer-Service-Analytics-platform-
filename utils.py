"""
Utility functions for text processing and analysis
"""
import logging
from typing import List, Dict, Tuple
from collections import Counter
import nltk
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

class TextProcessor:
    """Advanced text processing utilities"""
    
    def __init__(self):
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        self.stop_words = set(stopwords.words('english'))
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        text = text.strip().lower()
        text = ' '.join(text.split())
        return text
    
    @staticmethod
    def get_text_stats(text: str) -> Dict[str, int]:
        """Extract text statistics"""
        words = text.split()
        sentences = text.split('.')
        
        return {
            'total_words': len(words),
            'total_sentences': len([s for s in sentences if s.strip()]),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'unique_words': len(set(words))
        }
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """Extract top keywords from text"""
        words = [word for word in text.lower().split() 
                if word not in self.stop_words and len(word) > 3]
        word_freq = Counter(words)
        return word_freq.most_common(top_n)
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 512) -> List[str]:
        """Split text into chunks"""
        words = text.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            current_chunk.append(word)
            if len(' '.join(current_chunk)) >= chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
