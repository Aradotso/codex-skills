---
name: codex-candy-eval-benchmark
description: Benchmark and evaluate Codex/GPT models using a candy math puzzle with reasoning token analysis
triggers:
  - test codex model performance with candy puzzle
  - run candy eval benchmark on GPT models
  - evaluate reasoning tokens and accuracy
  - benchmark codex with candy math problem
  - run codex降智测试
  - analyze model reasoning effort vs correctness
  - batch test codex cli responses
  - evaluate gpt model candy puzzle accuracy
---

# Codex Candy Eval Benchmark

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A Python-based benchmarking tool that evaluates OpenAI Codex/GPT models using a standardized candy math puzzle. Measures reasoning token usage against answer correctness to assess model performance degradation patterns (降智测试).

## What It Does

- Batch tests Codex CLI with a specific candy distribution math problem
- Tracks reasoning token consumption across different effort levels
- Calculates accuracy rates by detecting the correct answer (21)
- Supports multiple reasoning effort levels: low, medium, high, xhigh
- Zero third-party dependencies - pure Python with Codex CLI integration

## Prerequisites

You must have [Codex CLI](https://github.com/openai/codex) installed and authenticated:

```bash
# Install Codex CLI (follow official instructions)
# Authenticate with your OpenAI credentials
codex auth login
```

## Installation

```bash
git clone https://github.com/haowang02/codex-candy-eval.git
cd codex-candy-eval
```

No additional dependencies required - uses only Python standard library.

## Key Commands

### Basic Usage

```bash
# Run single test with default settings (medium reasoning)
python codex_candy_eval.py

# Test specific model with high reasoning effort
python codex_candy_eval.py -m gpt-5.5 -r high

# Run 10 tests to get statistical accuracy
python codex_candy_eval.py -n 10

# Full benchmark with all parameters
python codex_candy_eval.py -m gpt-5.5 -r xhigh -n 20
```

### Command-Line Arguments

- `-m, --model`: Codex model name (e.g., `gpt-5.5`, `gpt-4`, defaults to local CLI default)
- `-r, --reasoning-effort`: Reasoning level - `low`, `medium`, `high`, `xhigh` (default: `medium`)
- `-n, --tests`: Number of test iterations (default: `1`)

## The Candy Puzzle

The benchmark uses a standardized math problem:

> "小明有5颗糖，小红比小明多3颗，小刚比小红多2倍。问小刚有多少颗糖？"
> 
> (Xiaoming has 5 candies, Xiaohong has 3 more than Xiaoming, Xiaogang has 2 times more than Xiaohong. How many candies does Xiaogang have?)

**Correct Answer:** 21

The script validates responses by checking if "21" appears as a standalone number in the output.

## Code Examples

### Running Programmatic Benchmarks

```python
import subprocess
import json
import re

def run_codex_eval(model="gpt-5.5", reasoning="medium", num_tests=5):
    """Run candy eval and parse results"""
    cmd = [
        "python", "codex_candy_eval.py",
        "-m", model,
        "-r", reasoning,
        "-n", str(num_tests)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def extract_accuracy(output):
    """Extract accuracy percentage from output"""
    match = re.search(r'(\d+\.?\d*)%', output)
    return float(match.group(1)) if match else None

# Compare reasoning levels
for effort in ['low', 'medium', 'high', 'xhigh']:
    output = run_codex_eval(reasoning=effort, num_tests=10)
    accuracy = extract_accuracy(output)
    print(f"{effort}: {accuracy}% accuracy")
```

### Typical Output Structure

```
Running test 1/5...
Reasoning tokens: 1234
Response contains correct answer: ✓

Running test 2/5...
Reasoning tokens: 1156
Response contains correct answer: ✗

...

Results:
Total tests: 5
Correct: 3
Accuracy: 60.0%
Average reasoning tokens: 1195
```

### Custom Test Implementation

```python
#!/usr/bin/env python3
import subprocess
import sys

CANDY_PROMPT = """小明有5颗糖，小红比小明多3颗，小刚比小红多2倍。问小刚有多少颗糖？

请详细说明你的推理过程。"""

def query_codex(prompt, model=None, reasoning="medium"):
    """Query Codex CLI directly"""
    cmd = ["codex", "query"]
    
    if model:
        cmd.extend(["--model", model])
    
    cmd.extend(["--reasoning-effort", reasoning])
    cmd.append(prompt)
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    return result.stdout

def validate_answer(response):
    """Check if response contains correct answer 21"""
    # Look for standalone "21" (not part of larger number)
    import re
    pattern = r'\b21\b'
    return bool(re.search(pattern, response))

# Usage
response = query_codex(CANDY_PROMPT, model="gpt-5.5", reasoning="high")
is_correct = validate_answer(response)
print(f"Correct: {is_correct}")
print(f"Response:\n{response}")
```

## Configuration

The script reads from Codex CLI's default configuration (`~/.codexrc` or equivalent). No additional config files needed.

### Environment Variables

If your Codex CLI uses environment variables:

```bash
export OPENAI_API_KEY="your-key-here"
export CODEX_MODEL="gpt-5.5"  # Optional default model
```

## Common Patterns

### Batch Comparison Across Models

```bash
# Test multiple models
for model in gpt-4 gpt-5 gpt-5.5; do
  echo "Testing $model..."
  python codex_candy_eval.py -m $model -r high -n 20 | tee results_$model.txt
done
```

### Reasoning Effort Analysis

```bash
# Compare reasoning levels for same model
for effort in low medium high xhigh; do
  python codex_candy_eval.py -m gpt-5.5 -r $effort -n 10
done
```

### Statistical Sampling

```bash
# Large sample for statistical significance
python codex_candy_eval.py -m gpt-5.5 -r medium -n 100 > benchmark_results.txt
```

## Troubleshooting

### "codex: command not found"

Ensure Codex CLI is installed and in PATH:

```bash
which codex
# If not found, reinstall or add to PATH
export PATH="$PATH:/path/to/codex/bin"
```

### Authentication Errors

Re-authenticate with Codex CLI:

```bash
codex auth logout
codex auth login
```

### Incorrect Detection Rate

The script uses regex `\b21\b` to detect standalone "21". If you get false negatives, check:

- Character encoding issues (script uses UTF-8)
- Model returning answer in different format (e.g., "twenty-one")
- Response being truncated

### Python Encoding Issues

If Chinese characters display incorrectly:

```bash
export PYTHONIOENCODING=utf-8
python codex_candy_eval.py -m gpt-5.5 -r high -n 5
```

## Expected Behavior

- **Correct Answer:** 21 (Xiaoming: 5, Xiaohong: 8, Xiaogang: 8×2+8 = 21)
- **Higher Reasoning Effort:** Generally increases accuracy but uses more tokens
- **Model Variations:** Different models show different accuracy patterns
- **Token Usage:** Typical range 800-2000 reasoning tokens per query
