import networkx as nx
import matplotlib.pyplot as plt
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
import pandas as pd

# Ensure nltk is ready
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def analyze_semantic_network(df_turns, target_word="frustrated", window_size=5, top_n=30):
    """
    Builds a co-occurrence graph centered around a target word.
    """
    user_turns = df_turns[df_turns['role'] == 'user']['content'].tolist()
    
    # Simple tokenization
    texts = [re.sub(r'[^\w\s]', '', t.lower()).split() for t in user_turns]
    
    stop_words = set(stopwords.words('english'))
    custom_stops = {
        'im', 'ive', 'dont', 'cant', 'user', 'assistant', 'model', 'claude', 'ai',
        'ill', 'id', 'thats', 'try', 'trying', 'got', 'getting', 'new', 'able', 'sure',
        'thanks', 'thank', 'please', 'help', 'would', 'could', 'should', 'think', 'know',
        'want', 'make', 'need', 'use', 'using', 'get', 'like', 'one', 'way', 'time',
        'good', 'much', 'see', 'also', 'really', 'right', 'yeah', 'go', 'bit', 'lot',
        'well', 'say', 'said', 'work', 'working', 'thing', 'things',
        # Interview Bias Words (User Request)
        'particularly', 'happening', 'made', 'frustrated', 'feel', 'felt', 'feeling',
        # Meta/Conversation Words (Phase 2)
        'situation', 'example', 'share', 'time'
    }
    stop_words.update(custom_stops)

    co_occurrence = Counter()
    
    for tokens in texts:
        for i, token in enumerate(tokens):
            # Check window around the token
            if token == target_word: # Optimization
                start = max(0, i - window_size)
                end = min(len(tokens), i + window_size + 1)
                
                window_tokens = tokens[start:i] + tokens[i+1:end]
                
                for neighbor in window_tokens:
                    # Filter: Stop words and short words (Strictness INCREASED)
                    if neighbor in stop_words or len(neighbor) < 4:
                        continue
                        
                    # Avoid self-loops and directionality duplication
                    pair = tuple(sorted((token, neighbor)))
                    co_occurrence[pair] += 1
                
    # Filter edges regarding target word
    # If target_word is provided, we prioritize edges connected to it, 
    # but we also want the general "context" of that word.
    
    G = nx.Graph()
    
    # Add substantial edges
    for (w1, w2), count in co_occurrence.most_common(500): # Check top 500 overall first
        if count > 6: # Threshold INCREASED (Aggressive)
            G.add_edge(w1, w2, weight=count)
            
    # Now extract the ego graph for the target word if it exists
    if target_word in G:
        try:
            # Radius 1 or 2 to see immediate context
            ego_G = nx.ego_graph(G, target_word, radius=1)
            return ego_G
        except:
            return G # Return whole graph if ego fails
    
    # If target word not found in top edges, try to search specifically for it in raw counts
    relevant_pairs = {pair: count for pair, count in co_occurrence.items() if target_word in pair}
    if relevant_pairs:
        SG = nx.Graph()
        for (w1, w2), count in Counter(relevant_pairs).most_common(top_n):
             SG.add_edge(w1, w2, weight=count)
        return SG
        
    return G

def visualize_network(G, target_word, output_file="semantic_network.png"):
    """
    Visualizes the semantic network graph.
    """
    plt.figure(figsize=(12, 12))
    
    # Gunakan k yang agak besar agar menyebar, tanpa pengaruh bobot pada posisi
    # User Request: k=3.5
    pos = nx.spring_layout(G, k=15.0, iterations=200, seed=42)
    
    # Hitung ketebalan garis dengan Batas Minimum
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    
    # SETTING KETEBALAN - PERBAIKAN USER
    min_width = 1.5      # Garis paling tipis = 1.5
    scale_factor = 6.0   # Garis paling tebal = 1.5 + 6.0 = 7.5
    
    widths = [min_width + (w / max_weight) * scale_factor for w in weights]
    
    # Gambar Node
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='#E6F3FF', edgecolors='#99CCFF')
    
    # Gambar Edge (Perhatikan alpha=0.5 agar transparansi membantu melihat tumpukan)
    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.5, edge_color='gray')
    
    # Gambar Label
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif", font_weight='bold',
                            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=2))
    
    plt.title(f"Semantic Context: Why are users '{target_word}'?", fontsize=16)
    plt.axis('off')
    
    # Save file and close (Required for main.py integration)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    return output_file

def get_top_connections(G, top_n=10):
    """
    Returns a DataFrame of the strongest connections (highest weights).
    """
    all_edges = []
    for u, v, data in G.edges(data=True):
        all_edges.append({
            'Word 1': u,
            'Word 2': v,
            'Weight': data['weight']
        })

    df_edges = pd.DataFrame(all_edges)
    if not df_edges.empty:
        df_edges = df_edges.sort_values(by='Weight', ascending=False).reset_index(drop=True)
        return df_edges.head(top_n)
    else:
        return pd.DataFrame(columns=['Word 1', 'Word 2', 'Weight'])

def check_kwic(df, word1, word2, limit=5):
    """
    Checks the Context (Key Word In Context) for two words to verify semantic relationship.
    Returns a list of strings (sentences/snippets).
    """
    matches = df[
        df['content'].str.lower().str.contains(word1.lower()) & 
        df['content'].str.lower().str.contains(word2.lower())
    ]
    
    snippets = []
    for text in matches['content'].head(limit):
        # find the index of the first word to give a good snippet 
        # (This is a simple version, returning the whole turn is safer for context)
        snippets.append(text.replace('\n', ' ').strip()[:200] + "...")
        
    return snippets
