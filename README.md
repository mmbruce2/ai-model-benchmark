# 🤖 AI Model Benchmark Analyzer

Analyzes **15 top AI models** across OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, and Alibaba. Benchmark scores (MMLU, Math, Coding, Reasoning), cost efficiency, and latency comparison.

## What It Does

- **15 models** tracked: GPT-4o, Claude 3.5, Gemini 2.0, Llama 3.1, o1, DeepSeek V3, Mistral, Qwen
- **Overall leader**: o1-preview 91.9 avg, Gemini 2.5 Pro 88.1, Claude 3.5 Sonnet 87.1
- **Best coding**: o1-preview 95.1%, Gemini 2.5 Pro 93.5%, Claude 3.5 Sonnet 92.1%
- **Best math**: o1-preview 87.2%, Gemini 2.5 Pro 80.1%, o1-mini 80.1%
- **Best reasoning**: o1-preview 93.5%, Claude 3.5 Sonnet 89.2%, Gemini 2.5 Pro 88.9%
- **Best value**: Llama 3.1 8B at 1732.5 pts/$ (only $0.04/1M tokens!)
- **Fastest**: Llama 3.1 8B at 200ms, Gemini 2.0 Flash at 300ms
- **4 charts**: overall ranking, cost vs performance, benchmark breakdown, latency vs performance

## Quick Start

```bash
pip install pandas matplotlib
python analyzer.py
```

## Key Findings

```
🏆 OVERALL LEADERBOARD:
   o1-preview: 91.9 avg (OpenAI)
   Gemini 2.5 Pro: 88.1 (Google)
   Claude 3.5 Sonnet: 87.1 (Anthropic)
   o1-mini: 86.3 (OpenAI)
   GPT-4o: 85.7 (OpenAI)

💻 CODING:
   o1-preview: 95.1% | Gemini 2.5 Pro: 93.5% | Claude 3.5: 92.1%

💰 BEST VALUE:
   Llama 3.1 8B: 1732 pts/$ (tiny model, massive value)
   Gemini 2.0 Flash: 1105 pts/$ (fast + cheap)

⚡ FASTEST:
   Llama 3.1 8B: 200ms | Gemini 2.0 Flash: 300ms

🏢 BY PROVIDER:
   OpenAI: 86.0 avg | Google: 85.5 | Anthropic: 82.5
```

## Data Source

Compiled from published benchmark results (MMLU, MATH, HumanEval, GPQA) across LMSYS, Artificial Analysis, and published model cards (2024-2025).

## Tech Stack

- Python 3
- pandas — data processing
- matplotlib — visualization