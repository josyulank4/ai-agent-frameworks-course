"""A transparent group-chat engine (Lesson 21 demo).

Implements AutoGen's organising ideas: conversable agents, speaker
selection, a message budget and explicit termination — the most
important line in a conversational system. Stdlib only.
"""
MAX_MESSAGES = 9
SCRIPT = [
    ("support", "error rate doubled after the 14:02 deploy; logs show payment timeouts"),
    ("engineer", "the deploy raised the payment client timeout from 2s to 200ms by typo"),
    ("reviewer", "confirmed in the diff; fix is a one-line revert, blast radius is checkout only"),
    ("support", "TERMINATE: root cause found, revert approved, customer update drafted"),
]
def select_speaker(history):
    order = ["support", "engineer", "reviewer", "support"]
    return order[len(history) % len(order)]
def run_chat():
    history = []
    for speaker, text in SCRIPT:
        if len(history) >= MAX_MESSAGES:
            history.append(("system", "budget exhausted: chat stopped"))
            break
        chosen = select_speaker(history)
        history.append((chosen, text))
        if "TERMINATE" in text:
            break
    return history
def main():
    history = run_chat()
    print("group chat: support incident room")
    for speaker, text in history:
        print(f"  {speaker}: {text}")
    print(f"messages used: {len(history)} (budget {MAX_MESSAGES})")
    print("termination: explicit TERMINATE token from support agent")
    print("group chat demo complete")
if __name__ == "__main__":
    main()
