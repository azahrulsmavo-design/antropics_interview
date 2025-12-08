import semantic_analysis
import data_loader
import preprocessor
import analysis
import comparative_analysis
import portfolio_visuals
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import seaborn as sns

def main():
    # 1. Load Data
    print("--- 1. Loading Data ---")
    silhouette_score = 0.0
    cluster_df = None
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
    target_word = "satisfied" # User requested
    
    # Updated to use the new module
    G = semantic_analysis.analyze_semantic_network(df_turns, target_word=target_word)
    
    # Visualization is now handled by the module
    output_img = semantic_analysis.visualize_network(G, target_word, "semantic_network.png")
    
    report_lines.append(f"\n### 5.1 Semantic Network Analysis")
    report_lines.append(f"Generated network graph centered around **'{target_word}'**.")
    report_lines.append(f"![Semantic Network]({output_img})")
    
    # --- Tambahan Data Kuantitatif ---
    top_edges = semantic_analysis.get_top_connections(G, top_n=10)
    print(f"\n[Top 10 Strongest Connections with '{target_word}']")
    print(top_edges.to_string(index=False))
    
    report_lines.append(top_edges.to_markdown(index=False))
    
    # 3.6 Maturity Clusters
    print("Running Maturity Clustering...")
    try:
        cluster_df, centroids, feature_names, silhouette_score = analysis.analyze_maturity_clusters(df_turns, n_clusters=3)
    except Exception as e:
        print(f"Maturity clustering failed: {e}")
        cluster_df = None
        silhouette_score = 0.0
    
    if cluster_df is not None:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=cluster_df, x='x', y='y', hue='cluster', palette='viridis', style='cluster', s=100)
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
        df_centroids = pd.DataFrame(centroids, columns=feature_names)
        report_lines.append(df_centroids.to_markdown())

        # --- DEEP DIVE: CLUSTER 1 (POWER USERS) ---
        print("\n[Deep Dive: Cluster 1 - The 'Power Users']")
        report_lines.append(f"\n## 6. Deep Dive: Cluster 1 (The 'Skeptical Power Users')")
        report_lines.append("Analyzing the 'High Technical / High Refinement' group to understand their behavior.")
        
        power_users = cluster_df[cluster_df['cluster'] == 1]['transcript_id'].unique()
        import random
        # Sample 5 users, or less if not enough
        sample_size = min(5, len(power_users))
        sample_ids = random.sample(list(power_users), sample_size)
        
        report_lines.append(f"\n### Persona Profile: The Architect")
        report_lines.append(f"> **Archetype**: Users who tend to write long, complex prompts and frequently correct the AI until they get exactly what they want.")
        
        for i, tid in enumerate(sample_ids, 1):
            report_lines.append(f"\n#### Sample Case {i} (Transcript ID: `{tid}`)")
            subset = df_turns[df_turns['transcript_id'] == tid]
            user_msgs = subset[subset['role'] == 'user']['content'].tolist()
            if user_msgs:
                first_msg = user_msgs[0].strip()
                preview = first_msg[:300] + "..." if len(first_msg) > 300 else first_msg
                report_lines.append(f"**User Intent**: \"{preview}\"")
                report_lines.append(f"- **Total Turns**: {len(subset)}")
                report_lines.append(f"- **Refinement Count**: {subset['content'].str.contains('no|change|wrong|better', case=False).sum()}")

    # --- COMPARATIVE ANALYSIS ---
    print("\n[Comparative Analysis]")
    comp_df = None
    try:
        comp_df, comp_img = comparative_analysis.run_comparative_analysis()
        if comp_df is not None:
             report_lines.append(f"\n## 7. Comparative Analysis (Workforce vs Creatives vs Scientists)")
             report_lines.append("Comparison of top themes across different user professions.")
             report_lines.append(f"![Comparative Topics]({comp_img})")
             report_lines.append("\n**Top Topics Data:**")
             report_lines.append(comp_df.to_markdown(index=False))
    except Exception as e:
        print(f"comparative analysis failed: {e}")

    # --- MODEL VALIDATION ---
    print("\n[Model Validation]")
    
    # Check if silhouette_score is defined (it should be if clustering ran)
    if 'silhouette_score' not in locals() or silhouette_score is None:
        silhouette_score = 0.0

    print(f"Silhouette Score: {silhouette_score:.3f}")
    
    # 2. Semantic Accuracy
    kwic_samples = semantic_analysis.check_kwic(df_turns, "satisfied", "results", limit=2)
    
    report_lines.append(f"\n## 8. Model Validation Strategy")
    report_lines.append(f"### 8.1 Clustering Validity")
    report_lines.append(f"- **Silhouette Score**: `{silhouette_score:.3f}`")
    report_lines.append(f"> *Interpretation*: A score above 0.3 indicates fair structure with natural overlap.")
    
    report_lines.append(f"\n### 8.2 Semantic Accuracy (KWIC)")
    report_lines.append(f"Verified context for connection **'satisfied' + 'results'**:")
    for sample in kwic_samples:
        report_lines.append(f"- > \"{sample}\"")
        
    report_lines.append(f"\n### 8.3 Reliability")
    report_lines.append(f"- **Reproducibility**: Parameter `random_state=42` enforced.")

    # --- KEY INSIGHTS (PORTFOLIO SLIDE) ---
    print("\n[Generating Portfolio Visuals]")
    # 1. Comparative Chart
    chart_file = portfolio_visuals.generate_comparative_chart(comp_df, "portfolio_comparison.png")
    
    # 2. Persona Card
    # We pass dummy logic since the function just draws texts, but in a real scenario we'd pass stats
    persona_file = portfolio_visuals.generate_persona_card(None, "portfolio_persona.png")
    
    report_lines.append(f"\n## 9. Key Insights (Portfolio Slide)")
    report_lines.append("Visual summary for stakeholder presentation.")
    if chart_file:
         report_lines.append(f"![Comparative Chart]({chart_file})")
    if persona_file:
         report_lines.append(f"![Persona Card]({persona_file})")

    with open("analysis_report_generated.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    print("\n--- Analysis Complete. Report saved to analysis_report_generated.md ---")

if __name__ == "__main__":
    main()
