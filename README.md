# 🤖 AI Model Benchmark Comparison Tool

Compares **20 real AI models** across MMLU, Math, Coding, and Reasoning benchmarks. Ranks by overall score, cost-effectiveness, and use case fit.

## What It Does

- **Ranks all 20 models** by weighted benchmark average
- **Best value picks** for each budget tier ($0.20, $1, $3, $15 per 1M tokens)
- **Use case matching**: coding vs reasoning vs knowledge tasks
- **Cost-performance tradeoff** visualization
- **Provider comparison**: OpenAI vs Anthropic vs Google vs Meta vs open-source

## Quick Start

```bash
pip install pandas matplotlib
python analyzer.py
```

## Key Findings

```
🏆 TOP 5 OVERALL:
   1. o1-preview     92.6  (OpenAI — reasoning king)
   2. o3-mini        88.0  (OpenAI — best value reasoning)
   3. Claude 3.5     84.7  (Anthropic — balanced)
   4. GPT-4o         84.5  (OpenAI — versatile)
   5. GPT-4 Turbo    83.0  (OpenAI — fast/cheap GPT-4)

💡 BEST BUDGET PICKS:
   Under $0.20/1M: Gemini 2.0 Flash (score 82.8!)
   Under $1.00/1M: Gemini 2.0 Flash
   Under $3.00/1M: o3-mini (88.0 — great reasoning)
```

## Benchmarks Used

- **MMLU**: Multi-task language understanding (85+ questions)
- **Math**: Graduate-level math (MATH dataset)
- **Coding**: HumanEval code generation
- **Reasoning**: Complex multi-step reasoning tasks

## Data Source

Benchmark scores based on published results from LMSYS Chatbot Arena, OpenLLM Leaderboard, and LiveBench. Scores represent published evaluation results as of early 2025.

## Tech Stack

- Python 3
- pandas — data processing
- matplotlib — visualization
