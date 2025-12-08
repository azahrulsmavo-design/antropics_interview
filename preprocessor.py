import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data (if not already present, handled in main usually, but safe to include)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def clean_text(text):
    """
    Basic text cleaning: lowercase, remove special characters (optional depending on analysis).
    """
    if not isinstance(text, str):
        return ""
    
    # Remove metadata headers if present (e.g., specific repeated intro lines)
    # The prompt mentioned: "Hi there! I'm Claude..." need to check if this is common.
    # For now, we'll keep it simple and refine based on improved observation.
    
    text = text.lower()
    return text

def segment_dialogue(transcript):
    """
    Parses a single transcript into turns.
    Assumes format 'User: ... Assistant: ...' or similar.
    Returns a list of dicts: [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
    """
    if not isinstance(transcript, str):
        return []

    # Regex to split mostly works, but we need to capture the split to know who said what.
    # Pattern looks for "User:" or "Assistant:" at the start of lines or preceded by newlines
    # Adjust regex based on actual data format visibility.
    # Assuming standard "User:" and "Assistant:" markers.
    
    # This regex splits by the demarcations but keeps them to identify sections
    parts = re.split(r'(User:|Assistant:)', transcript)
    
    turns = []
    current_role = None
    
    for part in parts:
        part = part.strip()
        if part == "User:":
            current_role = "user"
        elif part == "Assistant:":
            current_role = "assistant"
        elif part and current_role:
            turns.append({
                'role': current_role,
                'content': part
            })
            
    return turns

def process_dataframe(df):
    """
    Applies segmentation to the entire dataframe.
    """
    all_turns = []
    
    for _, row in df.iterrows():
        transcript_id = row.get('transcript_id', 'unknown')
        text = row.get('text', '')
        
        turns = segment_dialogue(text)
        for turn in turns:
            turn['transcript_id'] = transcript_id
            all_turns.append(turn)
            
    return pd.DataFrame(all_turns)
