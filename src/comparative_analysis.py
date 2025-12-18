import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import data_loader
import preprocessor
import analysis

def run_comparative_analysis():
    """
    Loads data for workforce, creative (creatives), and scientific (scientists) splits,
    calculates top TF-IDF terms for each, and generates a grouped bar chart.
    Returns:
        pd.DataFrame: Combined top terms data.
        str: Path to the generated plot.
    """
    splits = {
        'Workforce': 'workforce',
        'Creatives': 'creatives',
        'Scientists': 'scientists'
    }
    
    combined_data = []

    print("\n--- Starting Comparative Analysis ---")
    
    for label, split_name in splits.items():
        print(f"Processing {label} ({split_name})...")
        df = data_loader.load_data(split=split_name)
        
        if df is None or df.empty:
            print(f"Skipping {label}: Data not found.")
            continue
            
        # Segment
        df_turns = preprocessor.process_dataframe(df)
        
        # Get Top Terms
        top_terms = analysis.analyze_topics_tfidf(df_turns, top_n=10)
        
        # Add to list
        top_terms['Category'] = label
        combined_data.append(top_terms)
        
    if not combined_data:
        return None, None
        
    all_terms = pd.concat(combined_data)
    
    # Visualization: Grouped Bar Chart
    # We want to compare the rank or score of specific terms across categories.
    # However, different categories have different top terms.
    # We'll take the UNION of the top 5 terms from each category and plot their scores across all categories.
    
    top_5_per_cat = all_terms.groupby('Category').head(5)['term'].unique()
    target_terms = list(set(top_5_per_cat))
    
    # Filter all_terms to only include these target terms
    # But wait, we need scores for these terms even if they are NOT in the top 10 of other categories.
    # This would require re-running TF-IDF for specific terms, which is complex.
    # SIMPLIFICATION: We will just plot the Top 5 unique terms from each, and if a term is missing in a category, it just won't show or we treat as 0 (not ideal).
    # Better approach for visualization: "Top Terms by Profession" - 3 subplots.
    
    plt.figure(figsize=(15, 6))
    sns.barplot(data=all_terms, x='term', y='rank', hue='Category') # rank here is actually score/tfidf sum
    plt.title("Top Topic Keywords by Profession")
    plt.xticks(rotation=45)
    plt.ylabel("TF-IDF Score")
    plt.tight_layout()
    output_file = "output/comparative_topics.png"
    plt.savefig(output_file, dpi=300)
    plt.close()
    
    return all_terms, output_file
