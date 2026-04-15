"""
AI Model Benchmark Analyzer
Analyzes 15 top AI models (GPT-4o, Claude 3.5, Gemini 2.0, Llama 3.1, o1, etc.).
Benchmark scores (MMLU, Math, Coding, Reasoning), cost efficiency, and latency comparison.

Run: python analyzer.py
"""
import json
import pandas as pd
import matplotlib.pyplot as plt

def main():
    with open('models.json') as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    print("=" * 55)
    print("  AI MODEL BENCHMARK ANALYZER")
    print("  15 Models | GPT-4o, Claude, Gemini, Llama, o1")
    print("=" * 55)
    print(f"\nTotal models: {len(df)}")

    # Overall leaderboard
    df['avg_benchmark'] = (df['mmliu'] + df['math'] + df['coding'] + df['reasoning']) / 4
    print("\n🏆 OVERALL LEADERBOARD (avg MMLU/Math/Coding/Reasoning):")
    top = df.nlargest(5, 'avg_benchmark')
    for _, r in top.iterrows():
        params = f"{r['params_b']}B" if r['params_b'] else "?"
        print(f"   {r['name']} ({r['provider']}): {r['avg_benchmark']:.1f} avg | {params} params")

    # Coding king
    print("\n💻 BEST CODING:")
    coding = df.nlargest(5, 'coding')
    for _, r in coding.iterrows():
        print(f"   {r['name']}: {r['coding']}% | {r['provider']}")

    # Math king
    print("\n🧮 BEST MATH:")
    math = df.nlargest(5, 'math')
    for _, r in math.iterrows():
        print(f"   {r['name']}: {r['math']}% | {r['provider']}")

    # Reasoning
    print("\n🧠 BEST REASONING:")
    reason = df.nlargest(5, 'reasoning')
    for _, r in reason.iterrows():
        print(f"   {r['name']}: {r['reasoning']}% | {r['provider']}")

    # Best value (performance per dollar)
    print("\n💰 BEST VALUE (Performance per Dollar):")
    df['value_score'] = df['avg_benchmark'] / df['cost_per_1m']
    value = df.nlargest(5, 'value_score')
    for _, r in value.iterrows():
        print(f"   {r['name']}: {r['value_score']:.1f} pts/$ | ${r['cost_per_1m']}/1M tokens")

    # Fastest models
    print("\n⚡ FASTEST LATENCY:")
    fast = df.nsmallest(5, 'latency_ms')
    for _, r in fast.iterrows():
        print(f"   {r['name']}: {r['latency_ms']}ms | ${r['cost_per_1m']}/1M tokens")

    # By provider
    print("\n🏢 BY PROVIDER:")
    by_prov = df.groupby('provider').agg(
        models=('name', 'count'),
        avg_bench=('avg_benchmark', 'mean'),
        best_model=('avg_benchmark', 'max'),
    ).sort_values('avg_bench', ascending=False)
    for prov, row in by_prov.iterrows():
        print(f"   {prov}: {int(row['models'])} models | {row['avg_bench']:.1f} avg | best: {row['best_model']:.1f}")

    # o1 reasoning beast
    print("\n🚀 O1 REASONING BEAST:")
    o1 = df[df['name'].str.contains('o1')]
    for _, r in o1.iterrows():
        print(f"   {r['name']}: Reasoning {r['reasoning']}% | Coding {r['coding']}% | Math {r['math']}%")

    # Charts
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    prov_colors = {'OpenAI': '#10A37F', 'Anthropic': '#CC785C', 'Google': '#4285F4', 'Meta': '#0668E1', 'Mistral': '#EB5230', 'Alibaba': '#FF6A00', 'DeepSeek': '#0066CC'}

    # Chart 1: Overall benchmark bar
    top10 = df.nlargest(10, 'avg_benchmark').sort_values('avg_benchmark')
    cols1 = [prov_colors.get(p, 'gray') for p in top10['provider']]
    axes[0,0].barh(range(len(top10)), top10['avg_benchmark'], color=cols1)
    axes[0,0].set_yticks(range(len(top10)))
    axes[0,0].set_yticklabels([n[:18] for n in top10['name']], fontsize=8)
    axes[0,0].set_xlabel('Average Benchmark Score')
    axes[0,0].set_title('Top AI Models by Overall Score (Color=Provider)')

    # Chart 2: Cost vs Performance scatter
    c2 = [prov_colors.get(p, 'gray') for p in df['provider']]
    axes[0,1].scatter(df['cost_per_1m'] + 0.01, df['avg_benchmark'], c=c2, s=60, alpha=0.8)
    for _, r in df.iterrows():
        if r['avg_benchmark'] > 80 or r['cost_per_1m'] > 5:
            axes[0,1].annotate(r['name'][:12], (r['cost_per_1m']+0.1, r['avg_benchmark']+0.5), fontsize=6)
    axes[0,1].set_xscale('log')
    axes[0,1].set_xlabel('Cost per 1M tokens (log scale, $)')
    axes[0,1].set_ylabel('Average Benchmark')
    axes[0,1].set_title('Cost vs Performance (Color=Provider)')

    # Chart 3: Radar-style - top 5 models comparison
    categories = ['mmliu', 'math', 'coding', 'reasoning']
    top5 = df.nlargest(5, 'avg_benchmark')
    x = range(len(categories))
    for i, (_, r) in enumerate(top5.iterrows()):
        vals = [r['mmliu'], r['math'], r['coding'], r['reasoning']]
        axes[1,0].plot(x, vals, marker='o', label=r['name'][:15], linewidth=2, markersize=5)
    axes[1,0].set_xticks(x)
    axes[1,0].set_xticklabels(categories)
    axes[1,0].set_ylabel('Score (%)')
    axes[1,0].set_title('Top 5 Models: Benchmark Breakdown')
    axes[1,0].legend(fontsize=7)
    axes[1,0].set_ylim(50, 100)

    # Chart 4: Latency vs benchmark
    c4 = [prov_colors.get(p, 'gray') for p in df['provider']]
    axes[1,1].scatter(df['latency_ms'], df['avg_benchmark'], c=c4, s=60, alpha=0.8)
    for _, r in df.iterrows():
        if r['avg_benchmark'] > 85 or r['latency_ms'] < 500:
            axes[1,1].annotate(r['name'][:10], (r['latency_ms']+50, r['avg_benchmark']+0.5), fontsize=6)
    axes[1,1].set_xscale('log')
    axes[1,1].set_xlabel('Latency (ms, log scale)')
    axes[1,1].set_ylabel('Average Benchmark')
    axes[1,1].set_title('Latency vs Performance (Color=Provider)')

    plt.tight_layout()
    plt.savefig('ai_benchmark_analysis.png', dpi=150, bbox_inches='tight')
    print("\n📈 Chart saved: ai_benchmark_analysis.png")
    df.to_csv('models.csv', index=False)
    print("📄 Data saved: models.csv")

if __name__ == '__main__':
    main()