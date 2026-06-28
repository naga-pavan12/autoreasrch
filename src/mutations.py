import os
import openai
import json
from pydantic import BaseModel

class MutationProposal(BaseModel):
    rationale: str
    updated_prompt: str

def mutate_prompt(candidate_path: str, previous_score: float, run_logs: list, provider_type="openai", model_name="gpt-4o-mini", base_url=None) -> str:
    """
    Reads the current candidate prompt and asks the LLM meta-agent to propose an improved version.
    """
    if not os.path.exists(candidate_path):
        raise FileNotFoundError(f"Cannot mutate missing candidate: {candidate_path}")
        
    with open(candidate_path, "r") as f:
        current_prompt = f.read()
        
    provider_type = provider_type.lower()
    
    if provider_type == "openai":
        client = openai.OpenAI() if os.getenv("OPENAI_API_KEY") else None
    elif provider_type == "ollama":
        url = base_url or "http://localhost:11434/v1"
        client = openai.OpenAI(base_url=url, api_key="ollama")
    else:
        raise ValueError(f"Unsupported provider for mutation: {provider_type}")
        
    if not client:
        raise ValueError(f"Client for {provider_type} not configured properly (missing API key?)")
        
    system_inst = (
        "You are an expert prompt engineer optimizing a workflow for Product Managers.\n"
        "Your task is to review the current prompt template, its recent score, and the specific item-level failure logs, then output an improved version.\n"
        "Focus on instructions that improve reasoning, specificity, or grounding accuracy.\n"
        "Output the new raw prompt in the 'updated_prompt' field exactly as it should be written to the file."
    )
    
    summary_logs = []
    for log in run_logs[:10]: # Limit to 10 failures
        if log.get('score', 0) < 0.9:
            summary = f"ID: {log['id']} | Score: {log.get('score', 0):.2f}"
            if log.get('error'):
                summary += f" | ERROR: {log['error']}"
            elif log.get('metrics'):
                summary += f" | Grounding: {log['metrics'].get('evidence_grounding', 0):.1f} | Completeness: {log['metrics'].get('completeness', 0):.1f}"
            summary_logs.append(summary)

    failure_context = "\n".join(summary_logs) if summary_logs else "No major failures found, just generic tuning needed."
    user_inst = f"Current Eval Score: {previous_score}\n\nFailure Context:\n{failure_context}\n\nCurrent Template:\n{current_prompt}"
    
    if provider_type == "openai":
        response = client.beta.chat.completions.parse(
            model=model_name,
            messages=[
                {"role": "system", "content": system_inst},
                {"role": "user", "content": user_inst}
            ],
            response_format=MutationProposal,
            temperature=0.7
        )
        proposal = response.choices[0].message.parsed
        
    elif provider_type == "ollama":
        schema_json = MutationProposal.model_json_schema()
        augmented_system = f"{system_inst}\n\nYou MUST return a single valid JSON object matching exactly this schema:\n{json.dumps(schema_json)}"
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": augmented_system},
                {"role": "user", "content": user_inst}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        content = response.choices[0].message.content
        proposal = MutationProposal.model_validate_json(content)
    
    base, ext = os.path.splitext(candidate_path)
    new_path = f"{base}_m{ext}"
    with open(new_path, "w") as f:
        f.write(proposal.updated_prompt)
        
    print(f"\n[Mutation] Rationale: {proposal.rationale}")
    print(f"[Mutation] Saved new candidate to {new_path}\n")
    return new_path
