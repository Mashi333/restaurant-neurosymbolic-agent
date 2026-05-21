class StateManager:
    def __init__(self):
        self.state = {
            "current_goal": "food_selection",
            "extracted_entities": {},
            "history": []
        }
        
    def update_entities(self, new_entities):
        self.state["extracted_entities"].update(new_entities)
        
    def get_state(self):
        return self.state

state_manager = StateManager()
