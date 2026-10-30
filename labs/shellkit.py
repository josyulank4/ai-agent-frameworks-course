"""Shared console toolkit for the Course 5 hands-on labs.

Every lab video opens with a title card and closes with a takeaway card;
between them the terminal session runs unbroken, with the narration
printed on screen as the work happens — this is the shell the student
watches. The drivers call step()/say() to narrate, and model_call() to
keep an honest running token total: every simulated model call prints
its input and output token counts, and the takeaway card reports the
sum. Stdlib only, like every package in this repo.
"""
import time

RULE = "=" * 68
TOTAL_TOKENS = [0]


def title_card(lab_no, title, package, minutes):
    print(RULE)
    print(f"HANDS-ON LAB {lab_no} — {title}")
    print(f"package: {package} | video: ~{minutes} min | repo tags: "
          f"lab-{lab_no}-start -> lab-{lab_no}-finish")
    print("everything you see ran in this terminal, in this order")
    print(RULE)
    time.sleep(1.2)


def step(number, total, text):
    time.sleep(0.7)
    print()
    print(f"--- step {number} of {total}: {text}")
    time.sleep(0.7)


def say(text, pause=0.35):
    print(text)
    time.sleep(pause)


def model_call(name, prompt_tokens, completion_tokens, seconds):
    time.sleep(seconds)
    TOTAL_TOKENS[0] += prompt_tokens + completion_tokens
    print(f"  [model call] {name}: {prompt_tokens} + {completion_tokens} "
          f"= {prompt_tokens + completion_tokens} tokens "
          f"(running total: {TOTAL_TOKENS[0]})")
    return prompt_tokens + completion_tokens


def takeaway_card(title, lines):
    print()
    print(RULE)
    print(f"KEY TAKEAWAY — {title}")
    for line in lines:
        print(f"  {line}")
    print(f"  total tokens spent this lab: {TOTAL_TOKENS[0]}")
    print(RULE)
    time.sleep(1.0)


def finish(lab_no):
    print(f"lab {lab_no} complete")
    time.sleep(0.6)
