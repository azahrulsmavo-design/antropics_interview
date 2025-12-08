# 🛠️ Technical Report: Fundamental Code & Models
**Project**: Anthropic Interview Analysis
**Domain**: NLP, User Behavior Analysis, Data Visualization

---

## 1. Fundamental Code Structure
The project uses a modular **ETL (Extract, Transform, Load)** architecture implemented in Python 3.10+.

### 1.1 Core Modules
*   **`data_loader.py` (Extract)**: 
    *   Implements `load_dataset` from the `datasets` library (Hugging Face).
    *   Handles different dataset splits (`workforce`, `creatives`, `scientists`).
*   **`preprocessor.py` (Transform)**:
    *   Converts raw conversation text into specific **"turns"** (User vs AI rows).
    *   Fundamental for enabling user-centric analysis.
*   **`analysis.py` (Analyze)**:
    *   Contains the core logic for TF-IDF, Clustering, and Interaction tagging.
    *   Uses `sklearn` for heavy lifting and `pandas` for aggregation.
*   **`semantic_analysis.py` (Analyze - Graph)**:
    *   Dedicated module for Network Analysis.
    *   Uses `networkx` for graph building and `matplotlib` for custom visualization.

### 1.2 Data Flow
`Raw Data` -> `DataFrame (Turns)` -> `Feature Engineering (Length, Complexity)` -> `Models (TF-IDF, K-Means)` -> `Visualization`.

---

## 2. Analytical Models Used

### 2.1 Term Frequency-Inverse Document Frequency (TF-IDF)
*   **Purpose**: Topic Modeling.
*   **Why**: Unlike simple word counts, TF-IDF reduces the weight of common English words (the, a, is) and highlights unique, meaningful terms for each user group.
*   **Implementation**: `TfidfVectorizer(stop_words='english', max_features=100)`.

### 2.2 Semantic Network Analysis (Co-occurrence Graph)
*   **Purpose**: Understanding context around specific keywords (e.g., "Satisfied").
*   **Method**: 
    1.  **Sliding Window**: Scans text 5 words left/right of the target.
    2.  **Filtering**: Removes stops and short words (<4 chars).
    3.  **Graphing**: Nodes = Words, Edges = Co-occurrences.
    4.  **Layout**: Fruchterman-Reingold force-directed algorithm (`spring_layout`). 
    *   *Note*: Custom physics (`k=15.0`) were applied to prevent node overlaps.

### 2.3 K-Means Clustering
*   **Purpose**: User Segmentation (Behavioral Persona).
*   **Features Used**:
    1.  **Verbosity**: Average character length per turn.
    2.  **Complexity**: Vocabulary richness (Unique words / Total words).
    3.  **Refinement Rate**: Frequency of corrective keywords ('wrong', 'change').
    4.  **Tech Score**: Frequency of technical jargon ('code', 'api').
*   **Algorithm**: Unsupervised K-Means with `n_clusters=3`.
*   **Result**: Identified 3 distinct groups (Casuals, Pragmatists, Power Users).

### 2.4 Sentiment & Interaction Tagging (Rule-Based)
*   **Purpose**: Quantifying abstract concepts like "Trust" or "Delegation".
*   **Method**: Dictionary-based pattern matching.
    *   *Delegation*: "draft", "generate", "write".
    *   *Hallucination/Trust*: "wrong", "false", "error".
*   **Why**: Rule-based systems are often more reliable than LLM-judges for specific keyword density analysis in technical domains.

---

## 3. Reliability & Validity
*   **Silhouette Score**: Used to validate cluster separation (Result: ~0.38, indicating fair structure).
*   **KWIC (Key Word In Context)**: Manual spot-checks to ensure semantic edges represent true linguistic relationships.
*   **Reproducibility**: `random_state=42` enforced across all nondeterministic algorithms.
