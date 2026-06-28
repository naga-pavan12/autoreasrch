import os
from src.io_utils import read_json, read_yaml

class BenchmarkLoader:
    def __init__(self, benchmark_dir: str):
        self.benchmark_dir = benchmark_dir
        self.manifest_path = os.path.join(benchmark_dir, "benchmark_manifest.yaml")
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        if os.path.exists(self.manifest_path):
            return read_yaml(self.manifest_path)
        return {"items": []}

    def load_items(self) -> list:
        items = []
        # If manifest exists, use it
        if self.manifest.get("items"):
            for item_meta in self.manifest["items"]:
                item_path = os.path.join(self.benchmark_dir, item_meta["file"])
                gold_path = os.path.join(self.benchmark_dir, item_meta.get("gold_file", ""))
                
                item_data = read_json(item_path)
                if os.path.exists(gold_path):
                    item_data["gold"] = read_json(gold_path)
                
                items.append(item_data)
        else:
            # Fallback: list all json files in items/
            items_dir = os.path.join(self.benchmark_dir, "items")
            if os.path.exists(items_dir):
                for f in os.listdir(items_dir):
                    if f.endswith(".json"):
                        items.append(read_json(os.path.join(items_dir, f)))
        return items
