# Customizing Semantic Network Visualization

This guide details how to customize the `main.py` and `analysis.py` scripts to tailor the semantic network visualization to your specific needs.

## 🔧 1. Core Parameters (Direct Visual Impact)

### A. In `main.py` (Visualization Section)

```python
# a. Layout Physics Simulation (Spread of nodes)
pos = nx.spring_layout(
    G, 
    k=10.0,           # ↑ Increase for wider spacing (default: 8.0)
    iterations=1500,  # ↑ Increase for more stable layout (default: 1000)
    seed=42           # Change seed for different layout variations
)

# b. Node & Edge Appearance
node_size=2500       # ↑ Increase for larger nodes (default: 2000)
widths = [(w / max_weight) * 8 for w in weights]  # ↑ Change 5 → 8 for thicker edges

# c. Color & Style
node_color='salmon'  # Change node color (e.g., '#FF6B6B', 'skyblue')
edge_alpha=0.7       # ↑ Increase edge opacity (default: 0.4)
font_size=12         # ↑ Increase label font size
```

### B. In `analysis.py` (Graph Construction)

```python
# a. Weak Connection Filter (CRITICAL PARAMETER!)
if count > 4:  # ↓ Decrease from 6 → 4 to show MORE connections
    G.add_edge(w1, w2, weight=count)

# b. Target Word & Window Context
def analyze_semantic_network(
    df_turns, 
    target_word="anxiety",  # Change central word (e.g., "career", "skills")
    window_size=7           # ↑ Increase context window (default: 5)
):

# c. Stopwords Filter
custom_stops = {
    'work', 'job', 'career',  # ↑ REMOVE these if you want them in the graph
    'user', 'assistant'       # ↓ ADD irrelevant words here
}

# d. Minimum Word Length
if len(neighbor) < 3:  # ↓ Decrease from 4 → 3 to include shorter words
    continue
```

## 🎨 2. Advanced Visual Customization (Add to `main.py`)

### A. Dynamic Colors based on Node Degree
```python
# Add BEFORE nx.draw_networkx_nodes()
import matplotlib.pyplot as plt
degrees = dict(G.degree())
max_degree = max(degrees.values())
node_colors = [plt.cm.plasma(deg / max_degree) for deg in degrees.values()]  # Gradient color

# Replace node drawing line:
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color=node_colors, edgecolors='k')
```

### B. Smarter Labels
```python
# Add AFTER nx.draw_networkx_labels()
# Truncate long labels
labels = {}
for node in G.nodes():
    if len(node) > 10:
        labels[node] = node[:8] + "..."
    else:
        labels[node] = node

nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
```

### C. Dark Mode / High Quality Output
```python
# Add BEFORE plt.savefig()
plt.gca().set_facecolor('#1e1e1e')  # Dark background for contrast
plt.gcf().set_facecolor('#121212')  # Overall figure background

# When saving:
plt.savefig(
    "semantic_network.png", 
    dpi=600,                     # ↑ High quality print
    bbox_inches='tight',
    facecolor='#121212',         # Match background
    edgecolor='none'
)
```

## ⚙️ 3. Advanced Analysis Customization (In `analysis.py`)

### A. Smart Percentile Filtering (Instead of hard threshold)
```python
# Replace "if count > 6" with:
# Keep top 20% strongest connections only
all_weights = [count for (w1,w2), count in co_occurrence.items()]
threshold = np.percentile(all_weights, 80)  # ↑ Increase 80→90 for stricter filter
if count >= threshold:
    G.add_edge(w1, w2, weight=count)
```

### B. Adding New Features (e.g., Sentiment)
```python
# inside analyze_maturity_clusters():
positive_words = ['good', 'great', 'love', 'happy']
negative_words = ['bad', 'hate', 'frustrated', 'angry']
sentiment_score = sum(text.lower().count(w) for w in positive_words) - \
                 sum(text.lower().count(w) for w in negative_words)

# Add to features list:
user_features.append([avg_len, complexity, refinement_score, tech_score, sentiment_score])
```

## 🚀 4. Practical Customization Workflow

1.  **Start with Filtering**:
    Lower `count > 6` → `count > 3` in `analysis.py` to see *all* connections.
    *→ Run → Evaluate "semantic_network.png"*

2.  **Adjust Layout**:
    Increase `k=8.0` → `k=12.0` in `main.py` if nodes are clumping.
    *→ Run → Compare*

3.  **Community Coloring**:
    Add community detection (requires `python-louvain` or similar) + dynamic coloring.
    *→ Result: Automatically grouped clusters!*
