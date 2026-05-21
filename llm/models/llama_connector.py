"""
LLM Connector — supports three modes:
  - "local"  : Uses the locally cached meta-llama/Llama-3.2-3B-Instruct via HuggingFace transformers
  - "mock"   : Returns deterministic mock responses (no model needed, for pure unit testing)
  - anything else: treated as a litellm model name (e.g. "gpt-3.5-turbo", "gpt-4o")
"""

import json
import re
from config.settings import LLM_MODE, LOCAL_MODEL_ID, OPENAI_API_KEY

class LLMConnector:
    def __init__(self):
        self._pipeline = None

    def _load_local_pipeline(self):
        """Lazy-load the local Llama model pipeline only when first needed."""
        if self._pipeline is not None:
            return
        print(f"[LLM] Loading local model: {LOCAL_MODEL_ID} (this may take a moment...)")
        from transformers import pipeline, AutoTokenizer
        import torch

        # Use float32 on CPU; no device_map needed without GPU / accelerate
        self._tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_ID)
        self._pipeline = pipeline(
            "text-generation",
            model=LOCAL_MODEL_ID,
            tokenizer=self._tokenizer,
            dtype=torch.float32,
            # device_map is intentionally omitted — defaults to CPU
        )
        print("[LLM] Local model loaded successfully.")

    def generate(self, prompt: str, is_json: bool = False) -> str:
        mode = LLM_MODE.lower()

        # ── MOCK MODE ──────────────────────────────────────────────────────────
        if mode == "mock":
            if is_json:
                food_type = "food"
                m = re.search(r"User Input:\s*(.*)", prompt)
                if m:
                    text = m.group(1).lower()
                    for kw in ["pizza","burger","pasta","salad","soup","sandwich","sushi"]:
                        if kw in text:
                            food_type = kw
                            break
                return json.dumps({"food_type": food_type, "budget": 20, "vegetarian": False})
            return "I can help you with that. Here are my recommendations."

        # ── LOCAL LLAMA MODE ──────────────────────────────────────────────────
        if mode == "local":
            self._load_local_pipeline()

            if is_json:
                # Wrap prompt with a clear JSON instruction
                full_prompt = (
                    f"{prompt}\n\n"
                    "Respond ONLY with a valid JSON object. No explanation, no markdown fences, "
                    "just raw JSON."
                )
            else:
                full_prompt = prompt

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful restaurant assistant. Be concise and friendly. "
                        "When asked to produce JSON, respond only with the JSON object."
                    ),
                },
                {"role": "user", "content": full_prompt},
            ]

            output = self._pipeline(
                messages,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.3,
                top_p=0.9,
                pad_token_id=self._tokenizer.eos_token_id,
                return_full_text=False,
            )

            # HF pipeline returns a list; the last message is the assistant turn
            generated = output[0]["generated_text"]
            # Extract just the last assistant message
            if isinstance(generated, list):
                last = generated[-1]
                text = last.get("content", "") if isinstance(last, dict) else str(last)
            else:
                text = str(generated)

            if is_json:
                # Strip any markdown fences the model may have added
                text = re.sub(r"```(?:json)?", "", text).strip().strip("`").strip()
                try:
                    json.loads(text)   # validate
                    return text
                except json.JSONDecodeError:
                    # Try to extract the first {...} block
                    m = re.search(r"\{.*\}", text, re.DOTALL)
                    if m:
                        return m.group(0)
                    return "{}"
            return text.strip()

        # ── REMOTE LLM VIA LITELLM ────────────────────────────────────────────
        try:
            import litellm
            litellm.api_key = OPENAI_API_KEY
            response = litellm.completion(
                model=LLM_MODE,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"} if is_json else None,
            )
            return response.choices[0].message.content
        except Exception as e:
            fallback = f'{{"error": "{str(e)}"}}' if is_json else f"Error: {str(e)}"
            return fallback


# Singleton — imported across all modules
llm = LLMConnector()
