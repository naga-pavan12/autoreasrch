import os
import time
from src.benchmark import BenchmarkLoader
from src.providers import LLMProvider
from src.scoring import score_extraction, read_rubric
from src.tasks import get_schema_for_task
from src.strategy import get_strategy_context

class TaskRunner:
    def __init__(self, research_type: str, task_name: str, provider_type="openai", model_name="gpt-4o-mini", base_url=None):
        self.research_type = research_type
        self.task_name = task_name
        self.loader = BenchmarkLoader(research_type)
        self.provider = LLMProvider(provider_type, model_name, base_url)
        self.schema = get_schema_for_task(research_type, task_name)
        self.strategy_context = get_strategy_context()
        
    def run_candidate(self, candidate_path: str):
        if not os.path.exists(candidate_path):
            raise FileNotFoundError(f"Candidate file not found: {candidate_path}")
            
        with open(candidate_path, "r") as f:
            prompt_template = f.read()

        items = self.loader.load_items()
        if not items:
            print(f"No benchmark items for {self.research_type} / {self.task_name}. Run prepare.py first.")
            return {"eval_score": 0.0}, []
            
        rubric = read_rubric(self.research_type, self.task_name)
        item_logs = []
        total_score = 0.0
        
        print(f"Running {self.research_type}:{self.task_name} using {self.provider.provider_type} ({self.provider.model_name})...")
        
        system_prompt = f"{prompt_template}\n\nSTRATEGIC CONTEXT:\n{self.strategy_context}"
        
        for idx, item in enumerate(items):
            t_start = time.time()
            log = {"id": item.get("id", f"item_{idx}")}
            user_prompt = f"INPUT DATA:\n{item['input_text']}"
            
            try:
                result, usage = self.provider.execute_structured(system_prompt, user_prompt, self.schema)
                log["output"] = result.model_dump()
                
                # Scoring
                expected = item.get("expected_pain_points") or item.get("expected_problems") or item.get("expected_themes") or item.get("expected_opportunities") or []
                metric_breakdown = score_extraction(result, expected, item["input_text"], rubric)
                
                score = metric_breakdown["total_score"]
                log["score"] = score
                log["metrics"] = metric_breakdown
                log["usage"] = {"prompt": getattr(usage, "prompt_tokens", 0) if usage else 0, 
                                "completion": getattr(usage, "completion_tokens", 0) if usage else 0}
                total_score += score
                
                print(f"[{idx+1}/{len(items)}] ID: {log['id']} | Score: {score:.2f} | Time: {time.time()-t_start:.1f}s")
                
            except Exception as e:
                print(f"[{idx+1}/{len(items)}] Error: {e}")
                log["score"] = 0.0
                log["error"] = str(e)
                total_score += 0.0
                
            item_logs.append(log)
            
        avg_score = total_score / len(items) if items else 0.0
        return {"eval_score": avg_score, "total_items": len(items)}, item_logs
