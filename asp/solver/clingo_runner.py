import clingo
import os
import json

class ASPSolver:
    def __init__(self):
        self.rules_dir = os.path.join(os.path.dirname(__file__), "..", "rules")
        self.facts_dir = os.path.join(os.path.dirname(__file__), "..", "facts")
        
    def solve(self, budget=None, allergies=None):
        constraints_path = os.path.join(self.facts_dir, "user_constraints.lp")
        os.makedirs(self.facts_dir, exist_ok=True)
        with open(constraints_path, "w") as f:
            if budget:
                f.write(f"budget({budget}).\n")
            if allergies:
                for allergy in allergies:
                    f.write(f"allergic({allergy.lower()}).\n")
                    
        # Dynamically write menu facts from menu.json
        menu_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "menu", "menu.json")
        menu_facts_path = os.path.join(self.facts_dir, "menu_facts.lp")
        
        with open(menu_facts_path, "w") as f:
            try:
                with open(menu_path, "r") as mf:
                    menu_data = json.load(mf)
                    for item in menu_data:
                        item_id = item["name"].lower().replace(" ", "_")
                        f.write(f"price({item_id}, {item['price']}).\n")
                        if "ingredients" in item:
                            for ing in item["ingredients"]:
                                f.write(f"contains({item_id}, {ing.replace(' ', '_')}).\n")
            except Exception as e:
                pass
            
            f.write("valid(X) :- price(X, _), not invalid(X).\n")
            f.write("#show valid/1.\n")
            
        ctl = clingo.Control()
        ctl.load(os.path.join(self.rules_dir, "budget_rules.lp"))
        ctl.load(os.path.join(self.rules_dir, "allergy_rules.lp"))
        ctl.load(constraints_path)
        ctl.load(menu_facts_path)
        
        ctl.ground([("base", [])])
        
        valid_items = []
        def on_model(m):
            for symbol in m.symbols(shown=True):
                if symbol.name == "valid":
                    valid_items.append(str(symbol.arguments[0]))
                    
        result = ctl.solve(on_model=on_model)
        return valid_items, str(result)

solver = ASPSolver()
