from src.io_utils import read_file
import os

CONTEXT_DIR = "shared/company_context"

def get_strategy_context() -> str:
    files = ["company_goals.md", "target_segments.md", "product_strategy.md", "constraints.md"]
    context = []
    for f in files:
        path = os.path.join(CONTEXT_DIR, f)
        content = read_file(path)
        if content:
            context.append(f"## {f.replace('.md', '').replace('_', ' ').capitalize()}\n{content}")
    return "\n\n".join(context)
