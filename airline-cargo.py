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
            [("weather", "clear"), ("cargo", "light")],
            ("schedule", "on_time"),
            "Clear weather and light cargo allow on-time scheduling",
        )
    )

    kb.add_rule(
        Rule(
            "R2",
            [("weather", "storm"), ("cargo", "heavy")],
            ("schedule", "delayed"),
            "Storm weather and heavy cargo cause delay",
        )
    )

    kb.add_rule(
        Rule(
            "R3",
            [("weather", "fog"), ("cargo", "medium")],
            ("schedule", "rescheduled"),
            "Fog conditions may require rescheduling",
        )
    )

    kb.add_rule(
        Rule(
            "R4",
            [("schedule", "on_time")],
            ("status", "flight_ready"),
            "On-time schedule means flight is ready",
        )
    )

    kb.add_rule(
        Rule(
            "R5",
            [("schedule", "delayed")],
            ("status", "wait_for_clearance"),
            "Delayed schedule requires clearance wait",
        )
    )

    kb.add_rule(
        Rule(
            "R6",
            [("schedule", "rescheduled")],
            ("status", "assign_new_slot"),
            "Rescheduled flights need new time slot",
        )
    )

    return kb


def run_expert_system():

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)

    wm = WorkingMemory()

    wm.add_fact("weather", weather_var.get())
    wm.add_fact("cargo", cargo_var.get())

    kb = build_knowledge_base()

    engine = InferenceEngine(kb, wm)

    engine.forward_chain()

    output_box.insert(tk.END, "===== AIRLINE EXPERT SYSTEM =====\n\n")

    results = {
        "Weather": wm.get("weather"),
        "Cargo": wm.get("cargo"),
        "Schedule": wm.get("schedule"),
        "Status": wm.get("status"),
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

root.title("Airline Scheduling Expert System")

root.geometry("700x550")

root.configure(bg="#f2f2f2")

title = tk.Label(
    root,
    text="Airline Scheduling Expert System",
    font=("Arial", 18, "bold"),
    bg="#f2f2f2",
)

title.pack(pady=10)

input_frame = tk.Frame(root, bg="#f2f2f2")

input_frame.pack(pady=10)

# Weather

tk.Label(
    input_frame,
    text="Weather",
    font=("Arial", 11, "bold"),
    bg="#f2f2f2",
).grid(row=0, column=0, padx=10, pady=10)

weather_var = tk.StringVar(value="clear")

weather_dropdown = ttk.Combobox(
    input_frame,
    textvariable=weather_var,
    values=["clear", "storm", "fog"],
    state="readonly",
)

weather_dropdown.grid(row=0, column=1)

# Cargo

tk.Label(
    input_frame,
    text="Cargo Weight",
    font=("Arial", 11, "bold"),
    bg="#f2f2f2",
).grid(row=1, column=0, padx=10, pady=10)

cargo_var = tk.StringVar(value="light")

cargo_dropdown = ttk.Combobox(
    input_frame,
    textvariable=cargo_var,
    values=["light", "medium", "heavy"],
    state="readonly",
)

cargo_dropdown.grid(row=1, column=1)

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
    "Welcome to Airline Scheduling Expert System\n\n",
)

output_box.config(state=tk.DISABLED)

root.mainloop()
