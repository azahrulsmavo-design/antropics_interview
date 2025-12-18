import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import LatentDirichletAllocation # Optional if needed
import re

def analyze_topics_tfidf(df_turns, top_n=20):
    """
    Analyzes topics using TF-IDF on user turns.
    """
    user_turns = df_turns[df_turns['role'] == 'user']['content'].tolist()
    
    if not user_turns:
        return {}
    
    tfidf = TfidfVectorizer(stop_words='english', max_features=100)
    tfidf_matrix = tfidf.fit_transform(user_turns)
    feature_names = tfidf.get_feature_names_out()
    
    # Simple sum of scores to find top words
    sums = tfidf_matrix.sum(axis=0)
    data = []
    for col, term in enumerate(feature_names):
        data.append( (term, sums[0,col] ))
        
    ranking = pd.DataFrame(data, columns=['term','rank'])
    ranking = ranking.sort_values('rank', ascending=False)
    
    return ranking.head(top_n)

def analyze_interactions(df_turns):
    """
    Classifies interactions based on keywords/patterns in USER turns.
    """
    # Define keywords/patterns
    delegation_keywords = ['automate', 'write this code', 'generate', 'draft']
    collaboration_keywords = ['revise', 'change', 'update', 'not quite', 'better way']
    foundation_keywords = ['starting point', 'template', 'idea', 'inspiration']
    
    results = {
        'delegation': 0,
        'collaboration': 0,
        'foundation': 0,
        'total_user_turns': 0
    }
    
    user_df = df_turns[df_turns['role'] == 'user']
    results['total_user_turns'] = len(user_df)
    
    for text in user_df['content']:
        text_lower = text.lower()
        
        if any(k in text_lower for k in delegation_keywords):
            results['delegation'] += 1
        elif any(k in text_lower for k in collaboration_keywords):
            results['collaboration'] += 1
        elif any(k in text_lower for k in foundation_keywords):
            results['foundation'] += 1
            
    return results

def analyze_trust_issues(df_turns):
    """
    Simple keyword search for trust/error issues.
    """
    error_keywords = ['wrong', 'incorrect', 'hallucinat', 'error', 'mistake', 'false']
    
    count = 0
    user_df = df_turns[df_turns['role'] == 'user']
    
    for text in user_df['content']:
        if any(k in text.lower() for k in error_keywords):
            count += 1
            
    return count, len(user_df)

def analyze_future_outlook(df_turns):
    """
    Look for career/skill related discussion.
    """
    keywords = ['career', 'skill', 'future', 'replace', 'job', 'learn']
    
    mentions = []
    user_df = df_turns[df_turns['role'] == 'user']
    
    for text in user_df['content']:
        if any(k in text.lower() for k in keywords):
            mentions.append(text[:200] + "...") # Store snippet
            
    return mentions

import networkx as nx
from collections import Counter
import itertools
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import re # Added import re

# Ensure nltk is ready
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# analyze_semantic_network has been moved to semantic_analysis.py

def analyze_maturity_clusters(df_turns, n_clusters=3):
    """
    Segments users based on their interaction patterns.
    """
    # Group by Transcript ID (User)
    user_groups = df_turns[df_turns['role'] == 'user'].groupby('transcript_id')
    
    user_features = []
    user_ids = []
    
    for uid, group in user_groups:
        full_text = " ".join(group['content'].astype(str))
        
        # Feature 1: Verbosity (Avg length of turn)
        avg_len = group['content'].str.len().mean()
        
        # Feature 2: Complexity (Unique words / Total words)
        words = full_text.split()
        complexity = len(set(words)) / len(words) if words else 0
        
        # Feature 3: Review/Refinement (Mentions of 'change', 'wrong')
        refinement_keywords = ['change', 'wrong', 'mistake', 'revise', 'no', 'update']
        refinement_score = sum(full_text.lower().count(k) for k in refinement_keywords)
        
        # Feature 4: Technical Terms (proxy for technical role)
        tech_keywords = ['code', 'python', 'sql', 'data', 'function', 'api']
        tech_score = sum(full_text.lower().count(k) for k in tech_keywords)
        
        user_features.append([avg_len, complexity, refinement_score, tech_score])
        user_ids.append(uid)
        
    if not user_features:
        return None, None, None, None
        
    X = np.array(user_features)
    
    # Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    
    # Validation: Silhouette Score
    score = silhouette_score(X, labels)
    
    # Dimensionality Reduction for Visualization (2D)
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X)
    
    cluster_data = pd.DataFrame({
        'transcript_id': user_ids,
        'cluster': labels,
        'x': coords[:, 0],
        'y': coords[:, 1],
        'avg_len': X[:, 0],
        'complexity': X[:, 1],
        'refinement': X[:, 2],
        'tech_score': X[:, 3]
    })
    
    return cluster_data, kmeans.cluster_centers_, ["Avg Length", "Complexity", "Refinement", "Tech Score"], score
