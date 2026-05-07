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
            [("problem", "login_issue")],
            ("solution", "reset_password"),
            "Login issues require password reset",
        )
    )

    kb.add_rule(
        Rule(
            "R2",
            [("problem", "printer_issue")],
            ("solution", "check_printer"),
            "Printer issues require printer inspection",
        )
    )

    kb.add_rule(
        Rule(
            "R3",
            [("problem", "network_issue")],
            ("solution", "restart_router"),
            "Network issues require router restart",
        )
    )

    kb.add_rule(
        Rule(
            "R4",
            [("problem", "slow_system")],
            ("solution", "restart_computer"),
            "Slow systems require restart and cleanup",
        )
    )

    kb.add_rule(
        Rule(
            "R5",
            [("solution", "reset_password")],
            ("department", "account_support"),
            "Account support handles login issues",
        )
    )

    kb.add_rule(
        Rule(
            "R6",
            [("solution", "check_printer")],
            ("department", "hardware_support"),
            "Hardware support handles printer issues",
        )
    )

    kb.add_rule(
        Rule(
            "R7",
            [("solution", "restart_router")],
            ("department", "network_team"),
            "Network team handles internet issues",
        )
    )

    kb.add_rule(
        Rule(
            "R8",
            [("solution", "restart_computer")],
            ("department", "technical_support"),
            "Technical support handles slow systems",
        )
    )

    return kb


def run_expert_system():

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)

    wm = WorkingMemory()

    wm.add_fact("problem", problem_var.get())

    kb = build_knowledge_base()

    engine = InferenceEngine(kb, wm)

    engine.forward_chain()

    output_box.insert(tk.END, "===== HELP DESK EXPERT SYSTEM =====\n\n")

    results = {
        "Problem": wm.get("problem"),
        "Solution": wm.get("solution"),
        "Department": wm.get("department"),
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

root.title("Help Desk Expert System")

root.geometry("700x550")

root.configure(bg="#f2f2f2")

title = tk.Label(
    root,
    text="Help Desk Expert System",
    font=("Arial", 18, "bold"),
    bg="#f2f2f2",
)

title.pack(pady=10)

input_frame = tk.Frame(root, bg="#f2f2f2")

input_frame.pack(pady=10)

# Problem

tk.Label(
    input_frame,
    text="Problem",
    font=("Arial", 11, "bold"),
    bg="#f2f2f2",
).grid(row=0, column=0, padx=10, pady=10)

problem_var = tk.StringVar(value="login_issue")

problem_dropdown = ttk.Combobox(
    input_frame,
    textvariable=problem_var,
    values=[
        "login_issue",
        "printer_issue",
        "network_issue",
        "slow_system",
    ],
    state="readonly",
)

problem_dropdown.grid(row=0, column=1)

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
    root,
    wrap=tk.WORD,
    font=("Consolas", 11),
    bg="white",
)

output_box.pack(
    padx=15,
    pady=10,
    fill=tk.BOTH,
    expand=True,
)

output_box.insert(
    tk.END,
    "Welcome to Help Desk Expert System\n\n",
)

output_box.config(state=tk.DISABLED)

root.mainloop()
