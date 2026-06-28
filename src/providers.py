import os
import json
import openai
from pydantic import BaseModel
from typing import Type, Tuple, Any
from src.io_utils import read_text

class LLMProvider:
    def __init__(self, provider_config: dict):
        self.type = provider_config.get("type", "openai").lower()
        self.model = provider_config.get("model", "gpt-4o-mini")
        self.temperature = provider_config.get("temperature", 0.2)
        
        if self.type == "openai":
            self.client = openai.OpenAI()
        else:
            # Add Ollama or others here if needed
            self.client = None

    def render_prompt(self, template_path: str, input_text: str, context_dir: str = None) -> str:
        template = read_text(template_path)
        
        # Inject input_text
        prompt = template.replace("{{input_text}}", input_text)
        
        # Inject context files if context_dir is provided
        if context_dir and os.path.exists(context_dir):
            context_str = "\n## STRATEGIC CONTEXT\n"
            for f in sorted(os.listdir(context_dir)):
                if f.endswith(".md"):
                    content = read_text(os.path.join(context_dir, f))
                    context_str += f"\n### {f}\n{content}\n"
            prompt = prompt.replace("## Strategic Context", context_str)
            
        return prompt

    def execute_structured(self, prompt: str, schema_path: str = None) -> dict:
        """
        Executes a prompt and returns a structured JSON response.
        If schema_path is provided, it uses it for validation (conceptually).
        For simplicity, we'll use OpenAI default JSON mode or Tool calling.
        """
        if self.type == "openai":
            # For this MVP, we use the standard ChatCompletion with json_object format
            # In a production version, we would use JSON Schema or Pydantic models.
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=self.temperature
            )
            return json.loads(response.choices[0].message.content)
        return {}
