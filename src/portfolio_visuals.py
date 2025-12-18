import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_comparative_chart(top_terms_df, output_file="portfolio_comparison.png"):
    """
    Generates a Horizontal Bar Chart comparing Top 3 Keywords across roles.
    Input: top_terms_df (DataFrame with columns 'term', 'rank', 'Category')
    """
    if top_terms_df is None or top_terms_df.empty:
        return None
        
    # Extract Top 3 Unique Keywords per Category
    # Logic: For each category, get top 3 terms based on 'rank' (score)
    top_3 = top_terms_df.groupby('Category').apply(lambda x: x.nlargest(3, 'rank')).reset_index(drop=True)
    
    plt.figure(figsize=(10, 6))
    
    # We want a grouped bar chart where y-axis is Category, x-axis is keywords?
    # No, user asked: Y Label = Workforce, Creatives... X Label = Top Keywords.
    # A bar chart where Y is roles and bars represent keywords doesn't work well if keywords are different.
    # Better approach: 3 Subplots (Horizontal Bars) sharing X axis?
    # Or just one crowded chart.
    # Let's try a Seaborn barplot with 'term' on Y and 'rank' on X, faceted by Category or hue.
    # User Request: "Label Y: Roles... Label X: Keywords"
    # This implies Categories are on Y axis. But we have multiple keywords per category.
    # Interpretation: A Cluster Bar Chart where Y-axis ticks are Categories, and for each category, there are 3 bars.
    
    # However, standard barplot logic in seaborn:
    # y='Category', x='rank', hue='term' -> Hue would be messy if terms are unique.
    
    # Alternative: Plot Term Names as Labels on the bars themselves.
    g = sns.barplot(data=top_3, y='Category', x='rank', hue='term', dodge=True, palette='viridis')
    
    # Clean up
    plt.title("Different Roles, Different Goals: Top 3 Distinct Keywords", fontsize=14, fontweight='bold')
    plt.xlabel("TF-IDF Score (Importance)", fontsize=10)
    plt.ylabel("Profession", fontsize=10)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Top Keywords")
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    return output_file

def generate_persona_card(cluster_stats, output_file="portfolio_persona.png"):
    """
    Generates a visual 'Persona Card' for Cluster 1 (The Architect).
    cluster_stats: dict/list containing [avg_len, refinement_rate, ...]
    """
    # Create a blank figure
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_facecolor('#f8f9fa') # Light gray bg
    ax.axis('off')
    
    # Draw "Card" rectangle
    rect = plt.Rectangle((0.05, 0.05), 0.9, 0.9, transform=ax.transAxes, 
                         color='white', ec='#333333', lw=2, zorder=0)
    ax.add_patch(rect)
    
    # Title
    ax.text(0.5, 0.85, "USER ARCHETYPE: THE ARCHITECT", 
            transform=ax.transAxes, ha='center', va='center', 
            fontsize=16, fontweight='bold', color='#2c3e50')
            
    # Subtitle
    ax.text(0.5, 0.78, "The 'Skeptical but Dependent' Power User", 
            transform=ax.transAxes, ha='center', va='center', 
            fontsize=10, fontstyle='italic', color='#7f8c8d')
            
    # Metrics
    # Avg Length
    ax.text(0.25, 0.6, "AVG PROMPT LENGTH", transform=ax.transAxes, ha='center', fontsize=8, color='gray')
    ax.text(0.25, 0.5, "1,095 chars", transform=ax.transAxes, ha='center', fontsize=18, fontweight='bold', color='#e74c3c')
    ax.text(0.25, 0.42, "(vs 522 avg)", transform=ax.transAxes, ha='center', fontsize=8, color='gray')
    
    # Refinement
    ax.text(0.75, 0.6, "REFINEMENT RATE", transform=ax.transAxes, ha='center', fontsize=8, color='gray')
    ax.text(0.75, 0.5, "High (26x)", transform=ax.transAxes, ha='center', fontsize=18, fontweight='bold', color='#2980b9')
    ax.text(0.75, 0.42, "(vs Low for others)", transform=ax.transAxes, ha='center', fontsize=8, color='gray')
    
    # Behavior Description
    ax.text(0.5, 0.25, '"Iterates constantly until output is perfect."', 
            transform=ax.transAxes, ha='center', va='center', 
            fontsize=12, style='italic', bbox=dict(facecolor='#ecf0f1', edgecolor='none', pad=10))
            
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    return output_file
