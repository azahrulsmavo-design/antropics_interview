import data_loader
import preprocessor
import analysis
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import seaborn as sns

def main():
    # 1. Load Data
    print("--- 1. Loading Data ---")
    df = data_loader.load_data(split='workforce')
    if df is None:
        print("Failed to load data.")
        return

    # 2. Preprocessing
    print("\n--- 2. Preprocessing & Segmentation ---")
    # Clean raw text if needed (optional stage)
    # df['text'] = df['text'].apply(preprocessor.clean_text)
    
    # Segment into turns
    df_turns = preprocessor.process_dataframe(df)
    print(f"Total turns extracted: {len(df_turns)}")
    print(df_turns['role'].value_counts())
    
    # 3. Analysis
    print("\n--- 3. Running Analysis ---")
    
    report_lines = ["# Analysis Report: Anthropic Interviewer (Workforce Split)"]
    
    # 3.1 Topics
    print("\n[Topic Modeling]")
    top_terms = analysis.analyze_topics_tfidf(df_turns)
    report_lines.append("\n## 1. Topic & Use Case Analysis")
    report_lines.append("Top TF-IDF Terms in User Prompts (Potential Tasks):")
    report_lines.append(top_terms.to_markdown(index=False))
    
    # 3.2 Interactions
    print("\n[Interaction Patterns]")
    interaction_stats = analysis.analyze_interactions(df_turns)
    report_lines.append("\n## 2. Interaction Patterns")
    report_lines.append("| interaction_type | count |")
    report_lines.append("| --- | --- |")
    for k, v in interaction_stats.items():
        report_lines.append(f"| {k} | {v} |")
    
    # 3.3 Trust
    print("\n[Trust & Limitations]")
    error_count, total = analysis.analyze_trust_issues(df_turns)
    report_lines.append("\n## 3. Trust & Limitations")
    report_lines.append(f"- **Total User Turns Analyzed**: {total}")
    report_lines.append(f"- **Turns with Error/Hallucination Keywords**: {error_count}")
    report_lines.append(f"- **Percentage**: {error_count/total*100:.2f}%")
    
    
    # 3.4 Future
    print("\n[Future Outlook]")
    future_mentions = analysis.analyze_future_outlook(df_turns)
    report_lines.append("\n## 4. Future Outlook & Skills")
    report_lines.append(f"Found {len(future_mentions)} mentions regarding career/skills/future.")
    report_lines.append("\n### Sample Quotes (First 10):")
    for m in future_mentions[:10]:
        clean_m = m.replace('\n', ' ').strip()
        report_lines.append(f"- > \"{clean_m}\"")

    # --- ADVANCED ANALYSIS ---
    print("\n[Advanced Analysis]")
    report_lines.append("\n## 5. Advanced Analysis (Diagnostic & Predictive)")
    
    # 3.5 Semantic Network
    print("Running Semantic Network Analysis...")
    target_word = "frustrated" # User requested
    G = analysis.analyze_semantic_network(df_turns, target_word=target_word)
    
    plt.figure(figsize=(12, 10))
    
    # Physics Simulation Layout (Distance = Strength)
    # REVISION: Increased k to 0.5, changed seed
    pos = nx.spring_layout(G, k=0.5, weight='weight', iterations=100, seed=123)
    
    # Dynamic Edge Widths
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    widths = [(w / max_weight) * 5 for w in weights]
    
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue') # Increased node size
    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif", font_weight='bold')
    plt.title(f"Semantic Network around '{target_word}' (Distance = Strength)")
    plt.axis('off')
    plt.savefig("semantic_network.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    report_lines.append(f"\n### 5.1 Semantic Network Analysis")
    report_lines.append(f"Generated network graph centered around **'{target_word}'**.")
    report_lines.append(f"![Semantic Network](semantic_network.png)")
    
    # 3.6 Maturity Clusters
    print("Running Maturity Clustering...")
    cluster_df, centroids, feature_names = analysis.analyze_maturity_clusters(df_turns, n_clusters=3)
    
    if cluster_df is not None:
        import seaborn as sns
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=cluster_df, x='x', y='y', hue='cluster', palette='viridis', s=100)
        plt.title("AI Maturity Clusters (User Segmentation)")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend(title='Cluster')
        plt.savefig("maturity_clusters.png", dpi=300)
        plt.close()
        
        report_lines.append(f"\n### 5.2 AI Maturity Matrix (Clustering)")
        report_lines.append("Performed K-Means clustering (k=3) based on verbosity, complexity, refinement frequency, and technical terms.")
        report_lines.append("![Maturity Clusters](maturity_clusters.png)")
        
        # Describe clusters using centroids
        report_lines.append("\n**Cluster Centroids (Average Feature Values):**")
        report_lines.append("| Cluster | Avg Length | Complexity | Refinement Count | Tech Score |")
        report_lines.append("| --- | --- | --- | --- | --- |")
        for i, center in enumerate(centroids):
            vals = [f"{v:.2f}" for v in center]
            report_lines.append(f"| {i} | {vals[0]} | {vals[1]} | {vals[2]} | {vals[3]} |")

    with open("analysis_report_generated.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    print("\n--- Analysis Complete. Report saved to analysis_report_generated.md ---")

if __name__ == "__main__":
    main()
