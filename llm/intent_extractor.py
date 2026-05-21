from llm.models.llama_connector import llm
import json
import os

class IntentExtractor:
    def __init__(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompt_templates/intent_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                self.prompt_template = f.read()
        except FileNotFoundError:
            self.prompt_template = "Extract the intent as JSON for: {user_input}"

    def extract(self, user_input: str) -> dict:
        prompt = self.prompt_template.replace("{user_input}", user_input)
        response = llm.generate(prompt, is_json=True)
        try:
            return json.loads(response)
        except Exception:
            return {}

extractor = IntentExtractor()
