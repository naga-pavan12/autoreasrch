import os
from src.io_utils import read_yaml

class Config:
    def __init__(self, research_type: str):
        self.research_type = research_type
        self.config_path = f"research_types/{research_type}/config.yaml"
        self.data = self._load_data()
        
    def _load_data(self):
        if not os.path.exists(self.config_path):
            # Fallback for types without config yet
            return {
                "research_type": self.research_type,
                "paths": {
                    "prompts_dir": f"research_types/{self.research_type}/prompts",
                    "rubrics_dir": f"research_types/{self.research_type}/rubrics",
                    "schemas_dir": f"research_types/{self.research_type}/schemas",
                    "benchmark_dir": f"research_types/{self.research_type}/benchmark",
                    "outputs_dir": f"research_types/{self.research_type}/outputs",
                    "reports_dir": f"research_types/{self.research_type}/reports",
                    "company_context_dir": "shared/company_context"
                }
            }
        return read_yaml(self.config_path)

    def get_path(self, key: str) -> str:
        return self.data.get("paths", {}).get(key, "")

    def get_task_config(self, task_name: str) -> dict:
        return self.data.get("tasks", {}).get(task_name, {})

    def get_provider_config(self) -> dict:
        return self.data.get("provider", {"type": "openai", "model": "gpt-4o-mini", "temperature": 0.2})
