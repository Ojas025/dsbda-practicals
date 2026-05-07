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
            [("trend", "bullish"), ("risk", "low")],
            ("decision", "buy"),
            "Bullish market and low risk indicate buy decision",
        )
    )

    kb.add_rule(
        Rule(
            "R2",
            [("trend", "bearish"), ("risk", "high")],
            ("decision", "sell"),
            "Bearish market and high risk indicate sell decision",
        )
    )

    kb.add_rule(
        Rule(
            "R3",
            [("trend", "stable"), ("risk", "medium")],
            ("decision", "hold"),
            "Stable market and medium risk indicate hold decision",
        )
    )

    kb.add_rule(
        Rule(
            "R4",
            [("decision", "buy")],
            ("advice", "invest_now"),
            "Buy decision suggests immediate investment",
        )
    )

    kb.add_rule(
        Rule(
            "R5",
            [("decision", "sell")],
            ("advice", "avoid_loss"),
            "Sell decision suggests avoiding further loss",
        )
    )

    kb.add_rule(
        Rule(
            "R6",
            [("decision", "hold")],
            ("advice", "wait_for_changes"),
            "Hold decision suggests waiting for market changes",
        )
    )

    return kb


def run_expert_system():

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)

    wm = WorkingMemory()

    wm.add_fact("trend", trend_var.get())
    wm.add_fact("risk", risk_var.get())

    kb = build_knowledge_base()

    engine = InferenceEngine(kb, wm)

    engine.forward_chain()

    output_box.insert(tk.END, "===== STOCK MARKET EXPERT SYSTEM =====\n\n")

    results = {
        "Trend": wm.get("trend"),
        "Risk": wm.get("risk"),
        "Decision": wm.get("decision"),
        "Advice": wm.get("advice"),
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

root.title("Stock Market Expert System")

root.geometry("700x550")

root.configure(bg="#f2f2f2")

title = tk.Label(
    root,
    text="Stock Market Expert System",
    font=("Arial", 18, "bold"),
    bg="#f2f2f2",
)

title.pack(pady=10)

input_frame = tk.Frame(root, bg="#f2f2f2")

input_frame.pack(pady=10)

# Trend

tk.Label(
    input_frame,
    text="Market Trend",
    font=("Arial", 11, "bold"),
    bg="#f2f2f2",
).grid(row=0, column=0, padx=10, pady=10)

trend_var = tk.StringVar(value="bullish")

trend_dropdown = ttk.Combobox(
    input_frame,
    textvariable=trend_var,
    values=["bullish", "bearish", "stable"],
    state="readonly",
)

trend_dropdown.grid(row=0, column=1)

# Risk

tk.Label(
    input_frame,
    text="Risk Level",
    font=("Arial", 11, "bold"),
    bg="#f2f2f2",
).grid(row=1, column=0, padx=10, pady=10)

risk_var = tk.StringVar(value="low")

risk_dropdown = ttk.Combobox(
    input_frame,
    textvariable=risk_var,
    values=["low", "medium", "high"],
    state="readonly",
)

risk_dropdown.grid(row=1, column=1)

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
    "Welcome to Stock Market Expert System\n\n",
)

output_box.config(state=tk.DISABLED)

root.mainloop()
