# 🤖 AI Model Benchmark Analyzer

Analyzes **15 leading AI models** across MMLU (knowledge), HumanEval (coding), MATH (reasoning), GSM8K (grade school math), cost per token, and context window size.

## What It Does

- **15 top AI models**: o1-preview, Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro, Llama 3 70B, Mistral Large, and more
- **Overall best**: o1-preview 91.6% avg (OpenAI), Claude 3.5 Sonnet 88.0%, GPT-4o 86.0%
- **Best MMLU**: o1-preview 91.4%, Gemini 1.5 Pro 89.3%, Claude 3.5 Sonnet 88.7%
- **Best coding**: o1-preview 93.1%, Claude 3.5 Sonnet 92.0%, GPT-4o 90.2%
- **Best math reasoning**: o1-preview 89.3%, Claude 3.5 Sonnet 78.2%, GPT-4o 76.6%
- **Best value**: Gemini 1.5 Flash 922.4 score ($0.075/1M tokens, 78.4% avg)
- **Largest context**: Gemini 1M tokens, Claude 200K tokens
- **4 charts**: Performance ranking, cost vs performance, top 5 breakdown, context vs performance

## Quick Start

```bash
pip install pandas matplotlib
python run.py
```

## Key Findings

```
🏆 OVERALL BEST (avg benchmark):
   o1-preview: 91.6% | Claude 3.5 Sonnet: 88.0%
   GPT-4o: 86.0% | Gemini 1.5 Pro: 83.2%

💰 BEST VALUE (score/dollar):
   Gemini 1.5 Flash: 922.4 | $0.075/1M tokens
   Claude 3 Haiku: 256.0 | $0.25/1M tokens
   Llama 3 8B: 252.0 | $0.20/1M tokens

📏 LARGEST CONTEXT:
   Gemini 1.5 Pro/Flash: 1M tokens
   Claude 3 family: 200K tokens

🏢 BY PROVIDER (avg benchmark):
   OpenAI: 79.8% avg | Google: 78.0% | Anthropic: 77.9%
```

## Benchmarks Explained

- **MMLU**: Multi-task language understanding (knowledge test across 57 subjects)
- **HumanEval**: Python coding challenges (real code completions)
- **MATH**: Graduate-level math problem solving
- **GSM8K**: Grade school math word problems (8th grade level)

## Data Source

Benchmark scores from OpenCompass, Artificial Analysis, LMSYS Chatbot Arena, and provider-published evaluations (2023-2024).

## Tech Stack

- Python 3
- pandas — data processing
- matplotlib — visualization