import tkinter as tk
from tkinter import scrolledtext, ttk


class Rule:
    def __init__(self, name, conditions, conclusion, explanation):
        self.name = name
        self.conditions = conditions
        self.conclusion = conclusion
        self.explanation = explanation


class KnowledgeBase:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)


class WorkingMemory:
    def __init__(self):
        self.facts = {}

    def add_fact(self, attribute, value):
        self.facts[attribute] = value

    def get(self, attribute):
        return self.facts.get(attribute)

    def has(self, attribute, value):
        return self.facts.get(attribute) == value


class InferenceEngine:
    def __init__(self, kb, wm):
        self.kb = kb
        self.wm = wm
        self.explanations = []

    def forward_chain(self):

        changed = True

        while changed:
            changed = False

            for rule in self.kb.rules:
                if all(self.wm.has(a, v) for a, v in rule.conditions):
                    attr, val = rule.conclusion

                    if self.wm.get(attr) != val:
                        self.wm.add_fact(attr, val)

                        self.explanations.append(f"{rule.name}: {rule.explanation}")

                        changed = True


def build_knowledge_base():

    kb = KnowledgeBase()

    kb.add_rule(
        Rule(
            "R1",
            [("symptom", "fever"), ("cough", "yes")],
            ("disease", "flu"),
            "Fever and cough indicate flu",
        )
    )

    kb.add_rule(
        Rule(
            "R2",
            [("symptom", "headache"), ("vomiting", "yes")],
            ("disease", "migraine"),
            "Headache and vomiting indicate migraine",
        )
    )

    kb.add_rule(
        Rule(
            "R3",
            [("disease", "flu")],
            ("treatment", "rest_and_medicine"),
            "Flu requires rest and medicine",
        )
    )

    kb.add_rule(
        Rule(
            "R4",
            [("disease", "migraine")],
            ("treatment", "painkillers"),
            "Migraine requires painkillers",
        )
    )

    kb.add_rule(
        Rule(
            "R5",
            [("disease", "flu")],
            ("doctor", "general_physician"),
            "Visit general physician for flu",
        )
    )

    kb.add_rule(
        Rule(
            "R6",
            [("disease", "migraine")],
            ("doctor", "neurologist"),
            "Visit neurologist for migraine",
        )
    )

    return kb


def run_expert_system():

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)

    wm = WorkingMemory()

    wm.add_fact("symptom", symptom_var.get())
    wm.add_fact("cough", cough_var.get())
    wm.add_fact("vomiting", vomiting_var.get())

    kb = build_knowledge_base()

    engine = InferenceEngine(kb, wm)

    engine.forward_chain()

    output_box.insert(tk.END, "===== HOSPITAL EXPERT SYSTEM =====\n\n")

    results = {
        "Disease": wm.get("disease"),
        "Treatment": wm.get("treatment"),
        "Doctor": wm.get("doctor"),
    }

    for key, value in results.items():
        if value:
            value = value.upper().replace("_", " ")
        else:
            value = "UNKNOWN"

        output_box.insert(tk.END, f"{key:<12}: {value}\n")

    output_box.insert(tk.END, "\n===== REASONING TRACE =====\n\n")

    for explanation in engine.explanations:
        output_box.insert(tk.END, explanation + "\n")

    output_box.config(state=tk.DISABLED)


root = tk.Tk()

root.title("Hospital Expert System")

root.geometry("700x550")

root.configure(bg="#f2f2f2")

title = tk.Label(
    root, text="Hospital Expert System", font=("Arial", 18, "bold"), bg="#f2f2f2"
)

title.pack(pady=10)

input_frame = tk.Frame(root, bg="#f2f2f2")

input_frame.pack(pady=10)

# Symptom

tk.Label(
    input_frame, text="Main Symptom", font=("Arial", 11, "bold"), bg="#f2f2f2"
).grid(row=0, column=0, padx=10, pady=10)

symptom_var = tk.StringVar(value="fever")

symptom_dropdown = ttk.Combobox(
    input_frame,
    textvariable=symptom_var,
    values=["fever", "headache"],
    state="readonly",
)

symptom_dropdown.grid(row=0, column=1)

# Cough

tk.Label(input_frame, text="Cough", font=("Arial", 11, "bold"), bg="#f2f2f2").grid(
    row=1, column=0, padx=10, pady=10
)

cough_var = tk.StringVar(value="yes")

cough_dropdown = ttk.Combobox(
    input_frame, textvariable=cough_var, values=["yes", "no"], state="readonly"
)

cough_dropdown.grid(row=1, column=1)

# Vomiting

tk.Label(input_frame, text="Vomiting", font=("Arial", 11, "bold"), bg="#f2f2f2").grid(
    row=2, column=0, padx=10, pady=10
)

vomiting_var = tk.StringVar(value="no")

vomiting_dropdown = ttk.Combobox(
    input_frame, textvariable=vomiting_var, values=["yes", "no"], state="readonly"
)

vomiting_dropdown.grid(row=2, column=1)

# Button

analyze_button = tk.Button(
    root,
    text="Run Expert System",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    command=run_expert_system,
)

analyze_button.pack(pady=10)

# Output Box

output_box = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, font=("Consolas", 11), bg="white"
)

output_box.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

output_box.insert(tk.END, "Welcome to Hospital Expert System\n\n")

output_box.config(state=tk.DISABLED)

root.mainloop()
