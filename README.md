# PM Problem-Discovery Accelerator

**Transform raw research into strategic opportunities.**

A high-scale modular framework for Product Managers to synthesize qualitative data across 10 distinct research types.

## 🚀 Quick Start

1. Install dependencies
```bash
uv sync
```

2. Generate benchmark scenarios
```bash
python3 prepare.py
```

3. Run an experiment
```bash
python3 train.py --research-type customer_interviews --task extract_pain_points
```

## 🧠 Workflows Supported

We support 10 specialized research types, each with its own benchmark and local rules:
- `customer_interviews`
- `competitor_research`
- `support_tickets`
- `surveys`
- `sales_calls`
- `product_analytics`
- `market_trends`
- `win_loss_analysis`
- `feature_requests`
- `synthesis`

## 💻 Architecture

- `research_types/`: Task-specific prompts, benchmarks, and rubrics.
- `shared/`: Centralized context (Company Goals, Strategy) and global schemas.
- `src/`: Modular source code for providers, scoring, and execution logic.
- `runs/`: Detailed experiment reports.

## License
MIT
