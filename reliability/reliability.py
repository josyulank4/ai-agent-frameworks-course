"""Retries, circuit breakers and run budgets (Lesson 51 area / S11 demo).

Retries only where safe, a breaker that fails fast, and a run budget in
steps, tokens and money — whichever trips first stops the run. Stdlib.
"""
class Breaker:
    def __init__(self, threshold=3):
        self.failures, self.threshold, self.open = 0, threshold, False
    def call(self, fn):
        if self.open: return "breaker-open: failed fast"
        try:
            result = fn(); self.failures = 0; return result
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold: self.open = True
            return "call failed"
class Budget:
    def __init__(self, steps=20, tokens=20000, money=0.50):
        self.limits = {"steps": steps, "tokens": tokens, "money": money}
        self.used = {"steps": 0, "tokens": 0, "money": 0.0}
    def spend(self, steps=0, tokens=0, money=0.0):
        self.used["steps"] += steps; self.used["tokens"] += tokens; self.used["money"] += money
        for k, v in self.limits.items():
            if self.used[k] >= v: return f"budget tripped on {k}"
        return "within budget"
def flaky(fail_times):
    state = {"n": 0}
    def fn():
        state["n"] += 1
        if state["n"] <= fail_times: raise RuntimeError("provider 503")
        return "tool result ok"
    return fn
def retry(fn, attempts=3):
    for i in range(attempts):
        try: return fn(), i+1
        except Exception: continue
    return None, attempts
def main():
    print("reliability: retries, breaker, budgets")
    result, tries = retry(flaky(2))
    print(f"  retry: succeeded on attempt {tries} -> {result}")
    b = Breaker()
    dead = flaky(99)
    for _ in range(3): b.call(dead)
    print(f"  breaker after 3 failures: open={b.open}; next call -> {b.call(dead)}")
    budget = Budget()
    print(f"  budget after normal step: {budget.spend(steps=3, tokens=4000, money=0.02)}")
    print(f"  budget after runaway step: {budget.spend(steps=2, tokens=19000, money=0.01)}")
    print("reliability demo complete")
if __name__ == "__main__":
    main()
