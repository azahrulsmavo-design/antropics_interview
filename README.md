# Anthropic Interviewer Analysis Portfolio

![Portfolio Comparison Chart](output/portfolio_comparison.png)

This project provides an advanced analytical suite for the **"Anthropic Interviewer"** dataset. It goes beyond basic topic modeling to perform deep behavioral segmentation, comparative analysis across professional roles, and rigorous reliability testing.

## Key Capabilities

### 1. Behavior Comparison (Workforce vs Creatives vs Scientists)
We implemented a comparative analysis module to contrast vocabulary and intent across different dataset splits.
*   **Scientists**: Heavy use of `research`, `data`, `process`.
*   **Creatives**: Focus on `creative`, `project`, `sounds`.
*   **Workforce**: Operations-focused terms like `tasks`, `time`, `schedule`.

### 2. "Power User" Deep Dive (Cluster 1)
Using K-Means clustering, we identified a specific user persona: **"The Architect"**.
*   **Characteristics**: High verbosity (>1000 chars/prompt), high technical score, and frequent refinement loops (26x avg).
*   **Insight**: These users treat AI as a collaborative junior developer, constantly correcting and refining outputs.

### 3. Semantic Network Analysis
Visualizes the context of key emotions (e.g., "Satisfied", "Frustrated") using a force-directed graph.
*   **Features**: Custom stop-word removal (including interview bias words), edge weighting, and KWIC (Key Word in Context) verification.

### 4. Reliability & Validity
We don't just generate charts; we validate them.
*   **Silhouette Score**: Measures clustering validity (Score: ~0.38).
*   **Reproducibility**: Enforced `random_state=42` for consistent results.

---

## Project Structure

*   **`src/`**: Python source code.
    *   **`main.py`**: The orchestrator.
    *   **`analysis.py`**: Core logic.
    *   ...and other modules.
*   **`notebooks/`**: Jupyter notebooks (`anthropic_analysis_v2.ipynb`).
*   **`docs/`**: Documentation (`TECHNICAL_REPORT.md`, `analysis_report_generated.md`).
*   **`output/`**: Generated images and results.

---

## Installation & Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Analysis**:
    ```bash
    python src/main.py
    ```
    *Generates `docs/analysis_report_generated.md` and visual assets in `output/`.*

3.  **Explore the Notebook**:
    ```bash
    python src/generate_notebook.py
    ```
    *Creates `notebooks/anthropic_analysis_v2.ipynb`.*

---

## Outputs
Running the analysis produces:
*   `docs/analysis_report_generated.md`: Full insights report.
*   `output/portfolio_comparison.png`: Key Insights Chart.
*   `output/portfolio_persona.png`: "The Architect" Persona Card.
*   `output/semantic_network.png`: Word Co-occurrence Graph.
*   `output/maturity_clusters.png`: User Segmentation Scatter Plot.
