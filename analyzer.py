"""
AI Model Benchmark Comparison Tool
Compares 20 real AI models across MMLU, Math, Coding, Reasoning benchmarks.
Scores models by use case and cost-effectiveness.

Run: python analyzer.py
"""
import json
import pandas as pd
import matplotlib.pyplot as plt

def overall(row, weights=None):
    if weights is None:
        weights = {'mmlu': 0.25, 'math': 0.25, 'coding': 0.25, 'reasoning': 0.25}
    return sum(row[k] * v for k, v in weights.items())

def best_for_budget(df, budget_per_million):
    """Return best model under cost constraint."""
    candidates = df[df['cost_per_1m'] <= budget_per_million]
    if candidates.empty:
        return None
    return candidates.sort_values('overall', ascending=False).iloc[0]

def main():
    with open('models.json') as f:
        models = json.load(f)
    df = pd.DataFrame(models)

    print("=" * 55)
    print("  AI MODEL BENCHMARK COMPARISON TOOL")
    print(f"  {len(df)} models | MMLU, Math, Coding, Reasoning | Cost analysis")
    print("=" * 55)

    # Overall score
    df['overall'] = df.apply(overall, axis=1)

    # Rankings
    df_ranked = df.sort_values('overall', ascending=False).reset_index(drop=True)

    print("\n🏆 OVERALL BENCHMARK RANKINGS:")
    print(f"   {'Rank':4s}  {'Model':22s}  {'Overall':8s}  {'MMLU':6s}  {'Math':6s}  {'Code':6s}  {'Reason':7s}")
    for i, row in df_ranked.iterrows():
        print(f"   {i+1:3d}   {row['model']:22s}  {row['overall']:7.1f}  {row['mmlu']:5.1f}  {row['math']:5.1f}  {row['coding']:5.1f}  {row['reasoning']:6.1f}")

    # Best by category
    print("\n📊 BEST MODEL BY CATEGORY:")
    for col, label in [('mmlu','MMLU'), ('math','Math'), ('coding','Coding'), ('reasoning','Reasoning')]:
        best = df.loc[df[col].idxmax()]
        print(f"   {label:12s}: {best['model']:22s} ({best[col]:.1f})")

    # Cost analysis
    print("\n💰 BEST VALUE FOR MONEY (Score per $1M spent):")
    df['value_score'] = df['overall'] / df['cost_per_1m']
    df['value_per_dollar'] = df['overall'] / (df['cost_per_1m'] + 0.01)
    best_value = df.sort_values('value_score', ascending=False).head(5)
    for _, row in best_value.iterrows():
        per = f"${row['cost_per_1m']:.2f}" if row['cost_per_1m'] > 0 else "Free"
        print(f"   {row['model']:22s}: {row['overall']:5.1f} overall | {per}/1M tokens")

    # Budget picks
    print("\n💡 BUDGET PICKS:")
    for budget in [0.20, 1.00, 3.00, 15.00]:
        pick = best_for_budget(df, budget)
        if pick is not None:
            per = f"${budget:.2f}" if budget > 0 else "Free"
            print(f"   Under ${budget:.2f}/1M: {pick['model']} (score: {pick['overall']:.1f})")

    # OpenAI o1 analysis
    o1 = df[df['model'] == 'o1-preview'].iloc[0]
    print(f"\n🧠 o1-preview Special Case:")
    print(f"   Math: {o1['math']:.1f} | Reasoning: {o1['reasoning']:.1f} (state-of-the-art)")
    print(f"   But cost ${o1['cost_per_1m']:.0f}/1M — 3x GPT-4o for reasoning tasks")

    # Provider breakdown
    print("\n🏢 PROVIDER AVERAGE SCORES:")
    prov = df.groupby('provider')['overall'].agg(['mean','max','count']).sort_values('max', ascending=False)
    for p, row in prov.iterrows():
        print(f"   {p:12s}: avg {row['mean']:5.1f} | best {row['max']:5.1f} | {int(row['count'])} models")

    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Chart 1: Overall ranking
    df_sorted = df.sort_values('overall', ascending=True)
    colors = {'OpenAI': '#10a37f', 'Anthropic': '#d97706', 'Google': '#4285f4',
              'Meta': '#0081fb', 'Mistral': '#eb5c20', 'Alibaba': '#ff6a00',
              'DeepSeek': '#0066cc', 'Groq': '#4a154b', 'Perplexity': '#1f1f1f'}
    col_list = [colors.get(p, 'gray') for p in df_sorted['provider']]
    axes[0,0].barh(range(len(df_sorted)), df_sorted['overall'], color=col_list)
    axes[0,0].set_yticks(range(len(df_sorted)))
    axes[0,0].set_yticklabels(df_sorted['model'], fontsize=7)
    axes[0,0].set_xlabel('Overall Score (avg of 4 benchmarks)')
    axes[0,0].set_title('AI Model Benchmark Rankings')
    axes[0,0].axvline(x=80, color='red', linestyle='--', alpha=0.4)

    # Chart 2: MMLU vs Math scatter
    scatter_colors = [colors.get(p, 'gray') for p in df['provider']]
    scatter = axes[0,1].scatter(df['mmlu'], df['math'], c=scatter_colors, s=100, alpha=0.8)
    for _, row in df.iterrows():
        axes[0,1].annotate(row['model'][:12], (row['mmlu']+0.3, row['math']+0.3), fontsize=6)
    axes[0,1].set_xlabel('MMLU Score')
    axes[0,1].set_ylabel('Math Score')
    axes[0,1].set_title('MMLU vs Math Performance')
    # Legend for providers
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=v, label=k) for k, v in colors.items() if k in df['provider'].values]
    axes[0,1].legend(handles=legend_elements, fontsize=7, loc='lower right')

    # Chart 3: Cost vs Performance
    sizes = df['context'] / 2
    axes[1,0].scatter(df['cost_per_1m'], df['overall'], c=scatter_colors, s=sizes, alpha=0.7)
    for _, row in df.iterrows():
        axes[1,0].annotate(row['model'][:10], (row['cost_per_1m']+0.1, row['overall']+0.3), fontsize=6)
    axes[1,0].set_xlabel('Cost per 1M tokens ($)')
    axes[1,0].set_ylabel('Overall Score')
    axes[1,0].set_title('Cost vs Performance Tradeoff')
    axes[1,0].set_xscale('log')

    # Chart 4: Radar-style comparison (bar chart alternative)
    top5 = df.sort_values('overall', ascending=False).head(5)
    x = range(len(top5))
    width = 0.2
    for i, (col, label) in enumerate([('mmlu','MMLU'),('math','Math'),('coding','Coding'),('reasoning','Reasoning')]):
        axes[1,1].bar([xi + i*width for xi in x], top5[col], width, label=label)
    axes[1,1].set_xticks([xi + 1.5*width for xi in x])
    axes[1,1].set_xticklabels([m[:15] for m in top5['model']], rotation=20, fontsize=8)
    axes[1,1].set_ylabel('Score')
    axes[1,1].set_title('Top 5 Models — Breakdown by Benchmark')
    axes[1,1].legend(fontsize=8)
    axes[1,1].set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig('benchmark_comparison.png', dpi=150, bbox_inches='tight')
    print(f"\n📈 Chart saved: benchmark_comparison.png")
    df.to_csv('models.csv', index=False)
    print(f"📄 Data saved: models.csv")

if __name__ == '__main__':
    main()
