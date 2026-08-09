---
name: codex-complexity-optimizer
description: Analyze codebase complexity, identify performance hotspots, and generate safe optimization reports with risk assessments
triggers:
  - analyze code complexity in this project
  - find performance bottlenecks and optimization opportunities
  - generate a complexity optimization report
  - identify algorithmic complexity issues
  - show me performance hotspots in this codebase
  - optimize code complexity safely
  - find slow algorithms and recommend improvements
  - analyze time complexity of this code
---

# Codex Complexity Optimizer

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Codex Complexity Optimizer is a skill for analyzing codebases to identify algorithmic complexity issues, performance hotspots, and safe optimization opportunities. It produces detailed reports with file/line references, current complexity, recommended changes, expected improvements, risk levels, and required tests.

## Installation

Install globally via npm:

```bash
npm install -g codex-complexity-optimizer
```

The skill installs to:

```bash
${CODEX_HOME:-~/.codex}/skills/complexity-optimizer
```

Or run the installer directly:

```bash
npx codex-complexity-optimizer
```

## Core Functionality

The skill performs:

1. **Complexity Analysis** - Identifies O(n²), O(n³), and worse algorithmic complexity
2. **Performance Hotspot Detection** - Finds nested loops, inefficient data structures, redundant operations
3. **Safe Optimization Reports** - Categorizes changes by risk level (low/medium/high)
4. **Test Coverage Requirements** - Specifies tests/benchmarks needed before and after optimization
5. **Implementation Guidance** - Provides step-by-step optimization instructions

## Usage Patterns

### Basic Analysis

Request a complexity report:

```text
Use $complexity-optimizer to analyze this codebase and give me a report.
```

Analyze specific files or directories:

```text
Use $complexity-optimizer to check src/algorithms/ for performance issues.
```

### Applying Optimizations

The skill defaults to **report-only mode** and does not modify files unless explicitly requested.

Apply lowest-risk optimization:

```text
Use $complexity-optimizer to implement the lowest-risk optimization from the report and run the relevant tests.
```

Apply specific optimization:

```text
Use $complexity-optimizer to implement optimization #3 from the report.
```

### Focused Analysis

Target specific complexity types:

```text
Use $complexity-optimizer to find nested loops with O(n²) or worse complexity.
```

```text
Use $complexity-optimizer to identify redundant database queries in this module.
```

## Example Analysis Report

A typical report includes:

```python
# Optimization Report
# Generated: 2026-05-16

## Finding #1 - HIGH IMPACT, LOW RISK
File: src/data_processor.py
Line: 45-52
Current Complexity: O(n²)
Recommended Complexity: O(n)

### Current Code:
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates

### Recommended Change:
Use a set to track seen items in a single pass.

### Expected Improvement:
- Time complexity: O(n²) → O(n)
- For 10,000 items: ~50,000,000 ops → ~10,000 ops
- Estimated speedup: 5000x

### Risk Level: LOW
- Pure function, no side effects
- Simple algorithmic change
- Easy to verify correctness

### Required Tests:
1. Unit test with known duplicates
2. Test with empty list
3. Test with all unique items
4. Benchmark with 1k, 10k, 100k items

### Implementation:
```python
def find_duplicates(items):
    seen = set()
    duplicates = []
    for item in items:
        if item in seen and item not in duplicates:
            duplicates.append(item)
        seen.add(item)
    return duplicates
```
```

## Working with Python Projects

### Analyzing Python Code

The skill identifies common Python performance issues:

```python
# INEFFICIENT - O(n²)
def remove_duplicates_slow(data):
    result = []
    for item in data:
        if item not in result:  # List lookup is O(n)
            result.append(item)
    return result

# OPTIMIZED - O(n)
def remove_duplicates_fast(data):
    return list(dict.fromkeys(data))  # Preserves order, O(n)
```

### List Comprehension Optimization

```python
# INEFFICIENT - Multiple passes
filtered = [x for x in items if x > 0]
squared = [x ** 2 for x in filtered]
total = sum(squared)

# OPTIMIZED - Single pass
total = sum(x ** 2 for x in items if x > 0)
```

### Dictionary Lookups vs Loops

```python
# INEFFICIENT - O(n) lookup per iteration
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
for order in orders:
    user = next(u for u in users if u["id"] == order["user_id"])

# OPTIMIZED - O(1) lookup
users_by_id = {u["id"]: u for u in users}
for order in orders:
    user = users_by_id[order["user_id"]]
```

### Database Query N+1 Problem

```python
# INEFFICIENT - N+1 queries
def get_user_posts(user_ids):
    result = []
    for user_id in user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        posts = db.query(Post).filter(Post.user_id == user_id).all()
        result.append({"user": user, "posts": posts})
    return result

# OPTIMIZED - 2 queries total
def get_user_posts(user_ids):
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    posts = db.query(Post).filter(Post.user_id.in_(user_ids)).all()
    
    users_dict = {u.id: u for u in users}
    posts_by_user = {}
    for post in posts:
        posts_by_user.setdefault(post.user_id, []).append(post)
    
    return [
        {"user": users_dict[uid], "posts": posts_by_user.get(uid, [])}
        for uid in user_ids
    ]
```

## Configuration

The skill respects project-specific configuration in `.complexity-optimizer.json`:

```json
{
  "exclude": [
    "tests/",
    "build/",
    "node_modules/",
    "*.min.js"
  ],
  "thresholds": {
    "complexity_warn": "O(n²)",
    "complexity_error": "O(n³)",
    "cyclomatic_complexity": 15,
    "max_nesting_depth": 4
  },
  "risk_assessment": {
    "low": {
      "max_changes": 1,
      "requires_tests": true
    },
    "medium": {
      "requires_integration_tests": true,
      "requires_benchmark": true
    },
    "high": {
      "requires_review": true,
      "requires_full_test_suite": true
    }
  },
  "report_format": "markdown",
  "auto_fix": false
}
```

## Common Optimization Patterns

### String Concatenation

```python
# INEFFICIENT - O(n²) due to string immutability
result = ""
for item in items:
    result += str(item) + ","

# OPTIMIZED - O(n)
result = ",".join(str(item) for item in items)
```

### Set Operations

```python
# INEFFICIENT - O(n*m)
common = [x for x in list1 if x in list2]

# OPTIMIZED - O(n+m)
common = list(set(list1) & set(list2))
```

### Caching Expensive Computations

```python
from functools import lru_cache

# INEFFICIENT - Recomputes on every call
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# OPTIMIZED - Memoization
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Risk Assessment Guidelines

### Low Risk
- Pure functions with no side effects
- Simple algorithmic changes (loop → comprehension)
- Adding caching/memoization
- Replacing list with set for membership tests

### Medium Risk
- Database query optimization
- Changing data structures (list → dict)
- Batch processing changes
- Async/parallel processing introduction

### High Risk
- Multi-threaded/concurrent changes
- Critical path modifications
- External API interaction changes
- Core business logic alterations

## Troubleshooting

### Skill Not Detecting Issues

Ensure Python files are not in excluded paths:

```bash
# Check .complexity-optimizer.json exclude patterns
cat .complexity-optimizer.json | grep exclude
```

### False Positives

Override specific findings in `.complexity-optimizer.json`:

```json
{
  "ignore_patterns": [
    {
      "file": "src/legacy_system.py",
      "reason": "Optimization scheduled for v2.0 rewrite"
    }
  ]
}
```

### Verification After Optimization

Always run:

1. **Unit tests**: `pytest tests/`
2. **Integration tests**: `pytest tests/integration/`
3. **Benchmarks**: Compare before/after performance
4. **Memory profiling**: Check for memory regressions

Example benchmark:

```python
import timeit

# Before optimization
old_time = timeit.timeit(
    lambda: old_function(test_data),
    number=1000
)

# After optimization
new_time = timeit.timeit(
    lambda: new_function(test_data),
    number=1000
)

print(f"Speedup: {old_time / new_time:.2f}x")
```

## Integration with CI/CD

Run complexity analysis in CI:

```yaml
# .github/workflows/complexity-check.yml
name: Complexity Analysis
on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install -g codex-complexity-optimizer
      - run: complexity-optimizer analyze --fail-on-high-risk
```

## Best Practices

1. **Always benchmark** - Theoretical complexity improvements may not translate to real-world gains for small datasets
2. **Test thoroughly** - Even "safe" optimizations can introduce subtle bugs
3. **Profile first** - Focus on actual hotspots, not premature optimization
4. **Consider readability** - Sometimes O(n²) is acceptable if code is clearer
5. **Document trade-offs** - Explain why specific optimizations were or weren't applied

## License

MIT License - See project repository for details.
