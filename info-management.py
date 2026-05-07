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
            [("document_type", "student_record"), ("importance", "high")],
            ("storage", "secure_folder"),
            "Important student records need secure storage",
        )
    )

    kb.add_rule(
        Rule(
            "R2",
            [("document_type", "notes"), ("importance", "low")],
            ("storage", "shared_folder"),
            "Notes can be stored in shared folder",
        )
    )

    kb.add_rule(
        Rule(
            "R3",
            [("storage", "secure_folder"), ("user_role", "admin")],
            ("access", "granted"),
            "Admin can access secure folder",
        )
    )

    kb.add_rule(
        Rule(
            "R4",
            [("storage", "secure_folder"), ("user_role", "student")],
            ("access", "denied"),
            "Students cannot access secure folder",
        )
    )

    kb.add_rule(
        Rule(
            "R5",
            [("storage", "secure_folder")],
            ("backup", "daily"),
            "Secure folder requires daily backup",
        )
    )

    kb.add_rule(
        Rule(
            "R6",
            [("storage", "shared_folder")],
            ("backup", "weekly"),
            "Shared folder requires weekly backup",
        )
    )

    return kb


def run_expert_system():

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)

    wm = WorkingMemory()

    wm.add_fact("document_type", document_var.get())
    wm.add_fact("importance", importance_var.get())
    wm.add_fact("user_role", role_var.get())

    kb = build_knowledge_base()

    engine = InferenceEngine(kb, wm)

    engine.forward_chain()

    output_box.insert(tk.END, "===== EXPERT SYSTEM RESULT =====\n\n")

    results = {
        "Storage": wm.get("storage"),
        "Access": wm.get("access"),
        "Backup": wm.get("backup"),
    }

    for key, value in results.items():
        if value:
            value = value.upper().replace("_", " ")
        else:
            value = "UNKNOWN"

        output_box.insert(tk.END, f"{key:<10}: {value}\n")

    output_box.insert(tk.END, "\n===== REASONING TRACE =====\n\n")

    for explanation in engine.explanations:
        output_box.insert(tk.END, explanation + "\n")

    output_box.config(state=tk.DISABLED)


root = tk.Tk()

root.title("Information Management Expert System")

root.geometry("700x550")

root.configure(bg="#f2f2f2")

title = tk.Label(
    root,
    text="Information Management Expert System",
    font=("Arial", 18, "bold"),
    bg="#f2f2f2",
)

title.pack(pady=10)

input_frame = tk.Frame(root, bg="#f2f2f2")

input_frame.pack(pady=10)

# Document Type

tk.Label(
    input_frame, text="Document Type", font=("Arial", 11, "bold"), bg="#f2f2f2"
).grid(row=0, column=0, padx=10, pady=10)

document_var = tk.StringVar(value="student_record")

document_dropdown = ttk.Combobox(
    input_frame,
    textvariable=document_var,
    values=["student_record", "notes"],
    state="readonly",
)

document_dropdown.grid(row=0, column=1)

# Importance

tk.Label(input_frame, text="Importance", font=("Arial", 11, "bold"), bg="#f2f2f2").grid(
    row=1, column=0, padx=10, pady=10
)

importance_var = tk.StringVar(value="high")

importance_dropdown = ttk.Combobox(
    input_frame, textvariable=importance_var, values=["high", "low"], state="readonly"
)

importance_dropdown.grid(row=1, column=1)

# User Role

tk.Label(input_frame, text="User Role", font=("Arial", 11, "bold"), bg="#f2f2f2").grid(
    row=2, column=0, padx=10, pady=10
)

role_var = tk.StringVar(value="student")

role_dropdown = ttk.Combobox(
    input_frame, textvariable=role_var, values=["student", "admin"], state="readonly"
)

role_dropdown.grid(row=2, column=1)

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

output_box.insert(tk.END, "Welcome to Information Management Expert System\n\n")

output_box.config(state=tk.DISABLED)

root.mainloop()
