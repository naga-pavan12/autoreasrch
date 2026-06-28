import os
import json
from src.config import Config
from src.benchmark import BenchmarkLoader
from src.providers import LLMProvider
from src.scoring import Scorer
from src.reporting import Reporter
from src.io_utils import write_json, read_text

class TaskProcessor:
    def __init__(self, research_type: str, task_name: str, model_override: str = None):
        self.research_type = research_type
        self.task_name = task_name
        self.config = Config(research_type)
        
        # Load specific task config
        self.task_cfg = self.config.get_task_config(task_name)
        if not self.task_cfg:
            # Fallback if task is in prompts but not in config
            self.task_cfg = {"prompt_file": f"{task_name}.md"}
            
        provider_cfg = self.config.get_provider_config()
        if model_override:
            provider_cfg["model"] = model_override
            
        self.provider = LLMProvider(provider_cfg)
        self.loader = BenchmarkLoader(self.config.get_path("benchmark_dir"))
        
        rubric_path = os.path.join(self.config.get_path("rubrics_dir"), self.task_cfg.get("rubric_file", f"{task_name}.yaml"))
        self.scorer = Scorer(rubric_path)
        self.reporter = Reporter(self.config.get_path("reports_dir"))

    def run(self):
        items = self.loader.load_items()
        
        # Special case for synthesis: aggregate reports
        if self.research_type == "synthesis":
            items = self._aggregate_latest_reports()
            
        if not items:
            print(f"No benchmark items found for {self.research_type}")
            return

        run_results = []
        total_score = 0
        prompt_path = os.path.join(self.config.get_path("prompts_dir"), self.task_cfg["prompt_file"])
        context_dir = self.config.get_path("company_context_dir")

        for item in items:
            print(f"Processing item: {item.get('id', 'unknown')}...")
            
            input_text = item.get("input_text", "")
            prompt = self.provider.render_prompt(prompt_path, input_text, context_dir)
            
            # Execute LLM
            output = self.provider.execute_structured(prompt)
            
            # Score
            score_data = self.scorer.score(output, gold=item.get("gold"), input_text=input_text)
            
            item_result = {
                "id": item.get("id"),
                "input": input_text,
                "output": output,
                "scores": score_data
            }
            run_results.append(item_result)
            total_score += score_data["total_score"]
            
            # Save raw output
            output_filename = f"{item.get('id')}_{self.task_name}_output.json"
            write_json(os.path.join(self.config.get_path("outputs_dir"), output_filename), item_result)

        avg_score = total_score / len(items) if items else 0
        
        # Generate Report
        report_path = self.reporter.generate_report(
            self.research_type,
            self.task_name,
            self.task_cfg["prompt_file"],
            len(items),
            avg_score,
            run_results
        )
        
        print(f"Run completed. Average Score: {avg_score:.2f}")
        print(f"Full report at: {report_path}")

    def _aggregate_latest_reports(self) -> list:
        """
        Gathers all .md reports from the global reports/ directory
        and combines them into a single input item for synthesis.
        """
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            return []
            
        all_reports = sorted([f for f in os.listdir(reports_dir) if f.endswith(".md")], reverse=True)
        # For simplicity, let's just take the contents of all available reports
        combined_text = ""
        for r in all_reports:
            combined_text += f"\n--- Report: {r} ---\n"
            combined_text += read_text(os.path.join(reports_dir, r))
            
        if not combined_text:
            return []
            
        return [{
            "id": "aggregated_research_synthesis",
            "input_text": combined_text
        }]
