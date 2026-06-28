import os
from datetime import datetime
from src.io_utils import write_text

class Reporter:
    def __init__(self, reports_dir: str):
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_report(self, 
                       research_type: str, 
                       task: str, 
                       candidate: str, 
                       items_processed: int, 
                       aggregate_score: float, 
                       output_data: list) -> str:
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"report_{research_type}_{task}_{timestamp}.md"
        report_path = os.path.join(self.reports_dir, report_filename)
        
        lines = [
            f"# Problem Discovery Report",
            f"",
            f"## Run Summary",
            f"- Research type: {research_type}",
            f"- Task: {task}",
            f"- Candidate: {candidate}",
            f"- Items processed: {items_processed}",
            f"- Aggregate score: {aggregate_score:.1f} / 5.0",
            f"",
            f"## Top Findings Found",
            f""
        ]
        
        for item in output_data:
            # item is expected to have 'output' which is the JSON from LLM
            output_json = item.get("output", {})
            findings = output_json.get("problems", []) or output_json.get("pain_points", []) or output_json.get("opportunities", [])
            
            for i, f in enumerate(findings):
                lines.append(f"### {i+1}. {f.get('title', 'Untitled Finding')}")
                lines.append(f"- Severity: {f.get('severity', 'unknown')}")
                lines.append(f"- Strategic relevance: {f.get('strategic_relevance', 'unknown')}")
                lines.append(f"- Why it matters: {f.get('description', 'No description provided')}")
                lines.append(f"- Evidence:")
                for quote in f.get('evidence_quotes', []):
                    lines.append(f"  - \"{quote}\"")
                lines.append("")
                
        lines.append(f"## Scoring Notes")
        lines.append("- Heuristic-based evaluation of grounding and schema validity.")
        lines.append("- Strategic relevance check based on company goals.")
        lines.append("")
        lines.append(f"## Suggested Next Mutation")
        lines.append("Review failure cases in evidence grounding to tighten verbatim requirements.")

        content = "\n".join(lines)
        write_text(report_path, content)
        
        # Also copy to root reports/ for easy visibility
        root_reports_dir = "reports"
        os.makedirs(root_reports_dir, exist_ok=True)
        write_text(os.path.join(root_reports_dir, report_filename), content)
        
        return report_path
