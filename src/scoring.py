import os
import json
from src.io_utils import read_yaml

class Scorer:
    def __init__(self, rubric_path: str):
        self.rubric = read_yaml(rubric_path)
        self.dimensions = self.rubric.get("dimensions", [])

    def score(self, output: dict, gold: dict = None, input_text: str = "") -> dict:
        """
        Calculates scores based on rubric dimensions.
        """
        scores = {}
        total_weighted_score = 0
        
        # We'll use some simple heuristics for this prototype
        # In a real app, this could be another LLM call (LLM-as-a-judge)
        
        results = {}
        for dim in self.dimensions:
            name = dim["name"]
            weight = dim["weight"]
            
            # Implementation of heuristics
            score_val = self._calculate_heuristic(name, output, gold, input_text)
            
            results[name] = {
                "score": score_val,
                "weight": weight,
                "weighted": score_val * weight
            }
            total_weighted_score += score_val * weight
            
        return {
            "dimensions": results,
            "total_score": total_weighted_score,
            "max_score": 5.0 # standard scale
        }

    def _calculate_heuristic(self, dimension: str, output: dict, gold: dict, input_text: str) -> float:
        # Default starting score
        score = 3.0
        
        if dimension == "schema_validity":
            return 5.0 # If we got here, it's valid JSON
            
        elif dimension == "evidence_grounding":
            # Check if evidence_quotes in output exist in input_text
            extracted_items = output.get(list(output.keys())[0], [])
            all_quotes = []
            for item in extracted_items:
                all_quotes.extend(item.get("evidence_quotes", []))
            
            if not all_quotes: return 1.0
            
            hits = 0
            for quote in all_quotes:
                if quote.lower() in input_text.lower():
                    hits += 1
            
            return min(5.0, (hits / len(all_quotes)) * 5.0) if all_quotes else 3.0

        elif dimension == "specificity":
            # Very simple: based on description length
            extracted_items = output.get(list(output.keys())[0], [])
            avg_len = sum(len(i.get("description", "")) for i in extracted_items) / len(extracted_items) if extracted_items else 0
            if avg_len > 100: return 5.0
            if avg_len > 50: return 4.0
            return 2.0

        elif dimension == "strategy_alignment":
            # Check if keywords from goals appear in output reasons
            # (In a real system, you'd check alignment more deeply)
            return 4.0 # placeholder for MVP
            
        return 3.0 # default
