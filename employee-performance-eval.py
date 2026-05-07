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
            [("attendance", "high"), ("performance", "good")],
            ("rating", "excellent"),
            "High attendance and good performance indicate excellent rating",
        )
    )

    kb.add_rule(
        Rule(
            "R2",
            [("attendance", "medium"), ("performance", "good")],
            ("rating", "good"),
            "Medium attendance and good performance indicate good rating",
        )
    )

    kb.add_rule(
        Rule(
            "R3",
            [("attendance", "low"), ("performance", "average")],
            ("rating", "average"),
            "Low attendance and average performance indicate average rating",
        )
    )

    kb.add_rule(
        Rule(
            "R4",
            [("rating", "excellent")],
            ("promotion", "yes"),
            "Excellent yees are eligible for promotion",
        )
    )

    kb.add_rule(
        Rule(
            "R5",
            [("rating", "good")],
            ("promotion", "maybe"),
            "Good employees may be considered for promotion",
        )
    )

    kb.add_rule(
        Rule(
            "R6",
            [("rating", "average")],
            ("promotion", "no"),
            "Average employees are not eligible for promotion",
        )
    )

    return kb


def run_expert_system():

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)

    wm = WorkingMemory()

    wm.add_fact("attendance", attendance_var.get())
    wm.add_fact("performance", performance_var.get())

    kb = build_knowledge_base()

    engine = InferenceEngine(kb, wm)

    engine.forward_chain()

    output_box.insert(tk.END, "===== EMPLOYEE PERFORMANCE EXPERT SYSTEM =====\n\n")

    results = {
        "Attendance": wm.get("attendance"),
        "Performance": wm.get("performance"),
        "Rating": wm.get("rating"),
        "Promotion": wm.get("promotion"),
    }

    for key, value in results.items():
        if value:
            value = value.upper().replace("_", " ")
        else:
            value = "UNKNOWN"

        output_box.insert(tk.END, f"{key:<15}: {value}\n")

    output_box.insert(tk.END, "\n===== REASONING TRACE =====\n\n")

    for explanation in engine.explanations:
        output_box.insert(tk.END, explanation + "\n")

    output_box.config(state=tk.DISABLED)


root = tk.Tk()

root.title("Employee Performance Expert System")

root.geometry("700x550")

root.configure(bg="#f2f2f2")

title = tk.Label(
    root,
    text="Employee Performance Expert System",
    font=("Arial", 18, "bold"),
    bg="#f2f2f2",
)

title.pack(pady=10)

input_frame = tk.Frame(root, bg="#f2f2f2")

input_frame.pack(pady=10)

# Attendance

tk.Label(
    input_frame,
    text="Attendance",
    font=("Arial", 11, "bold"),
    bg="#f2f2f2",
).grid(row=0, column=0, padx=10, pady=10)

attendance_var = tk.StringVar(value="high")

attendance_dropdown = ttk.Combobox(
    input_frame,
    textvariable=attendance_var,
    values=["high", "medium", "low"],
    state="readonly",
)

attendance_dropdown.grid(row=0, column=1)

# Performance

tk.Label(
    input_frame,
    text="Performance",
    font=("Arial", 11, "bold"),
    bg="#f2f2f2",
).grid(row=1, column=0, padx=10, pady=10)

performance_var = tk.StringVar(value="good")

performance_dropdown = ttk.Combobox(
    input_frame,
    textvariable=performance_var,
    values=["good", "average"],
    state="readonly",
)

performance_dropdown.grid(row=1, column=1)

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
    "Welcome to Employee Performance Expert System\n\n",
)

output_box.config(state=tk.DISABLED)

root.mainloop()
