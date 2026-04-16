#!/usr/bin/env python3
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

data = [
    {"model": "GPT-4o", "provider": "OpenAI", "mmlu": 88.0, "humaneval": 90.2, "math": 76.6, "gsm8k": 89.4, "cost_per_million": 5.0, "context_window": 128000, "release_year": 2024},
    {"model": "GPT-4 Turbo", "provider": "OpenAI", "mmlu": 86.4, "humaneval": 85.4, "math": 64.3, "gsm8k": 83.6, "cost_per_million": 10.0, "context_window": 128000, "release_year": 2023},
    {"model": "GPT-3.5 Turbo", "provider": "OpenAI", "mmlu": 70.0, "humaneval": 76.6, "math": 42.5, "gsm8k": 57.1, "cost_per_million": 0.5, "context_window": 16385, "release_year": 2023},
    {"model": "Claude 3.5 Sonnet", "provider": "Anthropic", "mmlu": 88.7, "humaneval": 92.0, "math": 78.2, "gsm8k": 93.0, "cost_per_million": 3.0, "context_window": 200000, "release_year": 2024},
    {"model": "Claude 3 Opus", "provider": "Anthropic", "mmlu": 86.4, "humaneval": 84.9, "math": 67.1, "gsm8k": 78.4, "cost_per_million": 15.0, "context_window": 200000, "release_year": 2024},
    {"model": "Claude 3 Haiku", "provider": "Anthropic", "mmlu": 75.2, "humaneval": 75.2, "math": 47.4, "gsm8k": 68.4, "cost_per_million": 0.25, "context_window": 200000, "release_year": 2024},
    {"model": "Gemini 1.5 Pro", "provider": "Google", "mmlu": 89.3, "humaneval": 84.7, "math": 67.8, "gsm8k": 91.0, "cost_per_million": 1.25, "context_window": 1000000, "release_year": 2024},
    {"model": "Gemini 1.5 Flash", "provider": "Google", "mmlu": 85.9, "humaneval": 82.3, "math": 58.9, "gsm8k": 86.5, "cost_per_million": 0.075, "context_window": 1000000, "release_year": 2024},
    {"model": "Gemini 1.0 Pro", "provider": "Google", "mmlu": 83.6, "humaneval": 74.2, "math": 53.2, "gsm8k": 78.4, "cost_per_million": 1.0, "context_window": 32768, "release_year": 2023},
    {"model": "Llama 3 70B", "provider": "Meta", "mmlu": 82.0, "humaneval": 81.7, "math": 51.2, "gsm8k": 68.4, "cost_per_million": 0.9, "context_window": 8192, "release_year": 2024},
    {"model": "Llama 3 8B", "provider": "Meta", "mmlu": 68.4, "humaneval": 58.7, "math": 36.4, "gsm8k": 48.2, "cost_per_million": 0.2, "context_window": 8192, "release_year": 2024},
    {"model": "Mistral Large", "provider": "Mistral", "mmlu": 81.4, "humaneval": 80.0, "math": 52.1, "gsm8k": 66.4, "cost_per_million": 2.0, "context_window": 32000, "release_year": 2024},
    {"model": "Mistral 7B", "provider": "Mistral", "mmlu": 62.1, "humaneval": 51.2, "math": 28.4, "gsm8k": 38.4, "cost_per_million": 0.24, "context_window": 8000, "release_year": 2023},
    {"model": "Command R+", "provider": "Cohere", "mmlu": 77.8, "humaneval": 68.4, "math": 47.2, "gsm8k": 62.4, "cost_per_million": 3.0, "context_window": 128000, "release_year": 2024},
    {"model": "o1-preview", "provider": "OpenAI", "mmlu": 91.4, "humaneval": 93.1, "math": 89.3, "gsm8k": 92.4, "cost_per_million": 15.0, "context_window": 128000, "release_year": 2024},
]

with open('/tmp/ai-model-benchmark/models.json', 'w') as f:
    json.dump(data, f, indent=2)

df = pd.DataFrame(data)
df['avg_benchmark'] = df[['mmlu', 'humaneval', 'math', 'gsm8k']].mean(axis=1)
df['value_score'] = df['avg_benchmark'] / (df['cost_per_million'] + 0.01)

print("=" * 60)
print("  AI MODEL BENCHMARK ANALYZER")
print("  MMLU | HumanEval | MATH | GSM8K | Cost | Context")
print("=" * 60)
print(f"\nTotal models: {len(df)}")

print("\n🏆 OVERALL BEST (avg benchmark):")
for _, r in df.nlargest(5, 'avg_benchmark').iterrows():
    print(f"   {r['model']} ({r['provider']}): avg {r['avg_benchmark']:.1f}% | MMLU {r['mmlu']}% | HE {r['humaneval']}% | MATH {r['math']}% | GSM8K {r['gsm8k']}%")

print("\n🧠 BEST MMLU (knowledge):")
for _, r in df.nlargest(5, 'mmlu').iterrows():
    print(f"   {r['model']}: {r['mmlu']}%")

print("\n💻 BEST HumanEval (coding):")
for _, r in df.nlargest(5, 'humaneval').iterrows():
    print(f"   {r['model']}: {r['humaneval']}%")

print("\n📐 BEST MATH (math reasoning):")
for _, r in df.nlargest(5, 'math').iterrows():
    print(f"   {r['model']}: {r['math']}%")

print("\n🧮 BEST GSM8K (grade school math):")
for _, r in df.nlargest(5, 'gsm8k').iterrows():
    print(f"   {r['model']}: {r['gsm8k']}%")

print("\n💰 BEST VALUE (performance per dollar):")
for _, r in df.nlargest(5, 'value_score').iterrows():
    cost_str = f"${r['cost_per_million']:.3f}" if r['cost_per_million'] < 1 else f"${r['cost_per_million']:.1f}"
    print(f"   {r['model']}: value score {r['value_score']:.1f} | avg {r['avg_benchmark']:.1f}% | {cost_str}/1M tokens")

print("\n💸 CHEAPEST MODELS (under $0.50/1M tokens):")
for _, r in df.nsmallest(5, 'cost_per_million').iterrows():
    if r['cost_per_million'] <= 0.5:
        print(f"   {r['model']}: ${r['cost_per_million']:.3f}/1M | avg {r['avg_benchmark']:.1f}%")

print("\n📏 LARGEST CONTEXT WINDOWS:")
for _, r in df.nlargest(5, 'context_window').iterrows():
    ctx_str = str(int(r['context_window']//1000)) + 'K'
    print(f"   {r['model']}: {ctx_str} tokens")

print("\n🏢 BY PROVIDER (avg benchmark):")
by_prov = df.groupby('provider').agg(
    models=('model', 'count'),
    avg_bench=('avg_benchmark', 'mean'),
    best_model=('avg_benchmark', 'max'),
)
for prov, row in by_prov.sort_values('avg_bench', ascending=False).iterrows():
    print(f"   {prov}: {int(row['models'])} models | avg {row['avg_bench']:.1f}% | best {row['best_model']:.1f}%")

# Charts
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Chart 1: Avg benchmark by model
top = df.nlargest(12, 'avg_benchmark').sort_values('avg_benchmark')
provider_colors = {'OpenAI': '#10A37F', 'Anthropic': '#D2D2D2', 'Google': '#4285F4', 'Meta': '#0668E1', 'Mistral': '#EB7A00', 'Cohere': '#0F4C81'}
colors = [provider_colors.get(p, 'gray') for p in top['provider']]
axes[0,0].barh(range(len(top)), top['avg_benchmark'], color=colors)
axes[0,0].set_yticks(range(len(top)))
axes[0,0].set_yticklabels(top['model'], fontsize=9)
axes[0,0].set_xlabel('Average Benchmark Score (%)')
axes[0,0].set_title('AI Model Performance (Color=Provider)')
for i, v in enumerate(top['avg_benchmark']):
    axes[0,0].text(v+0.5, i, f'{v:.1f}%', va='center', fontsize=8)

# Chart 2: Cost vs performance
for prov, color in provider_colors.items():
    subset = df[df['provider'] == prov]
    axes[0,1].scatter(subset['cost_per_million'], subset['avg_benchmark'], c=color, label=prov, s=60, alpha=0.8)
axes[0,1].set_xlabel('Cost per Million Tokens ($)')
axes[0,1].set_ylabel('Avg Benchmark (%)')
axes[0,1].set_title('Cost vs Performance (lower-left = best value)')
axes[0,1].legend(fontsize=8)
axes[0,1].set_xscale('log')
for _, r in df.iterrows():
    if r['avg_benchmark'] > 85 or r['cost_per_million'] > 10:
        axes[0,1].annotate(r['model'][:12], (r['cost_per_million'], r['avg_benchmark']), fontsize=6)

# Chart 3: Radar-style comparison of top 5 (bar chart)
top5 = df.nlargest(5, 'avg_benchmark')
benchmarks = ['mmlu', 'humaneval', 'math', 'gsm8k']
x = range(len(top5))
width = 0.2
for i, (bench, label) in enumerate(zip(benchmarks, ['MMLU', 'HumanEval', 'MATH', 'GSM8K'])):
    vals = top5[bench].values
    axes[1,0].bar([xi + i*width for xi in x], vals, width=width, label=label)
axes[1,0].set_xticks([xi + 1.5*width for xi in x])
axes[1,0].set_xticklabels(top5['model'], fontsize=8, rotation=20, ha='right')
axes[1,0].set_ylabel('Benchmark Score (%)')
axes[1,0].set_title('Top 5 Models: Benchmark Breakdown')
axes[1,0].legend(fontsize=8)
axes[1,0].set_ylim(60, 100)

# Chart 4: Context window vs performance
for prov, color in provider_colors.items():
    subset = df[df['provider'] == prov]
    axes[1,1].scatter(subset['context_window']/1000, subset['avg_benchmark'], c=color, label=prov, s=60, alpha=0.8)
axes[1,1].set_xlabel('Context Window (K tokens)')
axes[1,1].set_ylabel('Avg Benchmark (%)')
axes[1,1].set_title('Context Window vs Performance')
axes[1,1].legend(fontsize=8)
axes[1,1].set_xscale('log')
for _, r in df.iterrows():
    if r['context_window'] > 500000 or r['avg_benchmark'] > 88:
        axes[1,1].annotate(r['model'][:12], (r['context_window']/1000, r['avg_benchmark']), fontsize=6)

plt.tight_layout()
plt.savefig('/tmp/ai-model-benchmark/ai_model_analysis.png', dpi=150, bbox_inches='tight')
print("\n📈 Chart saved: ai_model_analysis.png")
df.to_csv('/tmp/ai-model-benchmark/models.csv', index=False)
print("📄 Data saved: models.csv")
print("DONE")