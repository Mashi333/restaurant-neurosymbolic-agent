from llm.intent_extractor import extractor
from llm.response_generator import response_generator
from rag.retriever import retriever
from asp.solver.clingo_runner import solver
from conversation.state_manager import state_manager

class DialogManager:
    def process_message(self, user_input: str, user_context: dict = None):
        user_context = user_context or {}

        # 1. Extract structured intent via Llama
        intents = extractor.extract(user_input)
        state_manager.update_entities(intents)

        # 2. RAG: retrieve relevant menu/policy context
        rag_context, _ = retriever.retrieve_context(user_input, top_k=3)

        # 3. ASP: enforce constraints (budget, allergies)
        budget = user_context.get("budget") or intents.get("budget")
        allergies = user_context.get("allergies") or intents.get("allergies", [])
        valid_items, solve_status = solver.solve(budget=budget, allergies=allergies)

        # 4. Generate a natural language response using Llama
        response = response_generator.generate(
            user_input=user_input,
            rag_context=rag_context,
            valid_items=valid_items,
            user_context=user_context,
        )

        reasoning = {
            "extracted_intents": intents,
            "rag_context_preview": rag_context[:300] + "..." if len(rag_context) > 300 else rag_context,
            "asp_valid_items": valid_items,
            "asp_status": solve_status,
        }

        return response, reasoning

dialog_manager = DialogManager()
