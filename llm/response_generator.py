from llm.models.llama_connector import llm
import os

class ResponseGenerator:
    def __init__(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompt_templates/recommendation_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                self.prompt_template = f.read()
        except FileNotFoundError:
            self.prompt_template = "Recommend items based on: {user_input}"

    def generate(self, user_input: str, rag_context: str, valid_items: list, user_context: dict) -> str:
        # Convert asp_ids back to readable names
        readable_items = [item.replace("_", " ").title() for item in valid_items] if valid_items else []

        prompt = self.prompt_template.format(
            user_input=user_input,
            budget=user_context.get("budget", "any"),
            allergies=", ".join(user_context.get("allergies", [])) or "none",
            diet=user_context.get("diet", "None"),
            rag_context=rag_context if rag_context else "No specific menu info retrieved.",
            valid_items=", ".join(readable_items) if readable_items else "none that match your constraints"
        )
        return llm.generate(prompt, is_json=False)

response_generator = ResponseGenerator()
