# IMPLEMENTATION_GUIDE.md
## Project 1: Rule-Based AI Chatbot — Step-by-Step Build Guide
**DecodeLabs 2026 | For Intern Use**

---

## Overview

This guide walks you through building the chatbot in the correct order, explaining the *why* behind every decision. Follow it sequentially. Each phase builds on the last.

**Estimated time:** 1–2 hours for a complete, well-commented implementation.

---

## Phase 0: Setup

### 0.1 Create your file
```bash
mkdir decodelabs-project-1
cd decodelabs-project-1
touch chatbot.py
touch README.md
```

### 0.2 File header
Every professional script starts with a docstring. Add this at the top of `chatbot.py`:

```python
"""
chatbot.py
──────────
Project 1: Rule-Based AI Chatbot
DecodeLabs Industrial Training Kit | Batch 2026

Description:
    A deterministic, rule-based chatbot built using Python control flow
    and dictionary-based intent matching. This is the "Logic Engine" —
    a white-box system where every input-to-output path is fully traceable.

Architecture:
    - Input sanitization (strip + lowercase)
    - Dictionary knowledge base (O(1) lookup via .get())
    - Continuous while loop with explicit exit strategy
    - Fallback response for unrecognized inputs

Author: [Your Name]
Date:   [Date]
"""
```

---

## Phase 1: Constants & Configuration

Define all constants at the top, before any functions. This makes them easy to find and modify.

```python
# ── SECTION 1: CONFIGURATION ──────────────────────────────────────────────────

# The name displayed in the startup banner and responses
BOT_NAME = "DecodesBot"

# The set of strings that will terminate the program.
# Using frozenset for O(1) membership testing and immutability.
# NOTE: 'bye'/'goodbye' are intentionally NOT here — they are in the
# knowledge base and return a farewell response but keep the bot running.
# Only 'quit' and 'exit' actually stop the program.
EXIT_COMMANDS = frozenset({"quit", "exit"})

# The fallback response for any input not found in the knowledge base.
# This must NEVER be an empty string.
FALLBACK_RESPONSE = (
    "I don't understand that yet. "
    "Type 'help' to see what I can do."
)
```

**Why `frozenset`?**  
A `frozenset` is like a `set` but immutable (cannot be changed at runtime). The `in` operator on a set/frozenset is O(1) — a hash lookup, same as a dictionary key. Using a list would be O(n) and could be accidentally mutated.

---

## Phase 2: The Knowledge Base

This is the heart of your chatbot. Every intent your bot understands lives here.

```python
# ── SECTION 2: KNOWLEDGE BASE ─────────────────────────────────────────────────
#
# This dictionary IS your chatbot's "brain" for this project.
# Keys   → normalized user input (must be lowercase, stripped)
# Values → exact response string to display
#
# Design Rule: To add a new intent, add ONE line here. Nothing else changes.
# This is the O(1) pattern — lookup time is constant regardless of size.

KNOWLEDGE_BASE = {
    # ── Greetings ──────────────────────────────────────────────────────────
    "hello":            "Hello! How can I help you today?",
    "hi":               "Hey there! What can I do for you?",
    "hey":              "Hi! Ask me anything.",
    "good morning":     "Good morning! Ready to learn about AI?",
    "good evening":     "Good evening! How can I assist?",

    # ── Status ─────────────────────────────────────────────────────────────
    "how are you":      "I'm a rule-based system — no feelings, just logic. Running perfectly!",
    "are you okay":     "All systems nominal. 100% deterministic and operational.",

    # ── Identity ───────────────────────────────────────────────────────────
    "who are you":      f"I am {BOT_NAME}, a rule-based AI assistant at DecodeLabs.",
    "what is your name": f"My name is {BOT_NAME}. Nice to meet you!",
    "name":             f"I go by {BOT_NAME}.",

    # ── AI Knowledge ───────────────────────────────────────────────────────
    "what is ai":       (
        "AI (Artificial Intelligence) is the simulation of human intelligence "
        "processes by computer systems. It includes learning, reasoning, and self-correction."
    ),
    "what is machine learning": (
        "Machine learning is a subset of AI where systems learn from data "
        "to improve their performance without being explicitly programmed."
    ),
    "what is a chatbot":    "A chatbot is a software program that simulates human conversation.",
    "what is a rule based system": (
        "A rule-based system uses predefined if-else logic to make decisions. "
        "It is deterministic — the same input always gives the same output."
    ),

    # ── Help / Navigation ──────────────────────────────────────────────────
    "help":             (
        "Here's what I understand:\n"
        "  • hello / hi / hey        → greeting\n"
        "  • how are you             → status check\n"
        "  • who are you / name      → my identity\n"
        "  • what is ai              → AI definition\n"
        "  • what is machine learning → ML definition\n"
        "  • what is a chatbot       → chatbot definition\n"
        "  • thanks / thank you      → you're welcome\n"
        "  • quit / exit             → end session"
    ),
    "what can you do":  "I can answer questions about AI basics. Type 'help' for the full list.",

    # ── Courtesy ───────────────────────────────────────────────────────────
    "thanks":           "You're welcome! Is there anything else I can help with?",
    "thank you":        "Happy to help! Let me know if you have more questions.",
    "ok":               "Great! What else would you like to know?",
    "okay":             "Perfect! Anything else?",

    # ── Farewells (return response but do NOT exit — see EXIT_COMMANDS) ────
    "bye":              "Goodbye! It was great talking with you. (Tip: type 'quit' to exit.)",
    "goodbye":          "See you later! Type 'quit' when you want to end the session.",
    "see you":          "See you! Come back anytime.",
}
```

---

## Phase 3: The Core Logic Function

This is a **pure function** — it takes input, returns output. No printing, no loops, no side effects.

```python
# ── SECTION 3: CORE LOGIC ─────────────────────────────────────────────────────

def get_response(clean_input: str) -> str:
    """
    Look up the response for a given (already sanitized) user input.

    This function uses dictionary .get() — a single atomic O(1) operation
    that performs both the lookup AND provides the fallback default.

    Args:
        clean_input (str): Normalized user input (lowercased, stripped).
                           Must not be empty (caller's responsibility).

    Returns:
        str: The matched response, or FALLBACK_RESPONSE if no match found.
             Never returns None or an empty string.
    """
    # dict.get(key, default):
    #   - If key EXISTS in dict → returns dict[key]
    #   - If key MISSING        → returns default (FALLBACK_RESPONSE)
    # One line. One operation. O(1). This replaces an entire if-elif ladder.
    return KNOWLEDGE_BASE.get(clean_input, FALLBACK_RESPONSE)
```

**Why separate from the loop?**  
- `get_response()` can be imported and called in tests without launching the chatbot
- It has no side effects — easy to reason about
- It can be upgraded (e.g., add regex pre-processing) without touching the loop

---

## Phase 4: The Main Loop (The Heartbeat)

```python
# ── SECTION 4: RUNTIME ────────────────────────────────────────────────────────

def run_chatbot() -> None:
    """
    Main chatbot loop. Handles all I/O and orchestrates the IPO cycle.

    Loop structure (per iteration):
        1. Read raw input from stdin
        2. Sanitize: strip whitespace + lowercase
        3. Guard 1: handle empty input
        4. Guard 2: handle exit commands
        5. Get response via get_response()
        6. Print response to stdout
        7. Repeat

    Termination: only via EXIT_COMMANDS (step 4 → break).
    """

    # ── Startup Banner ────────────────────────────────────────────────────
    print("=" * 50)
    print(f"  {BOT_NAME} — Rule-Based AI Chatbot")
    print(f"  Powered by DecodeLabs | Batch 2026")
    print(f"  Type 'help' for available commands.")
    print(f"  Type 'quit' or 'exit' to end the session.")
    print("=" * 50)
    print()

    # ── Main Loop ─────────────────────────────────────────────────────────
    # This 'while True' is the heartbeat of the chatbot.
    # It runs indefinitely until an EXIT_COMMAND breaks it.
    while True:

        # ── Step 1: Read Input ─────────────────────────────────────────
        raw_input = input("You: ")

        # ── Step 2: Sanitize ───────────────────────────────────────────
        # .strip() removes leading/trailing whitespace (spaces, tabs, newlines)
        # .lower() converts all characters to lowercase
        # Result: "  Hello  " → "hello", "WHAT IS AI" → "what is ai"
        clean_input = raw_input.strip().lower()

        # ── Guard 1: Empty Input ───────────────────────────────────────
        # If the user pressed Enter with nothing typed (or only spaces),
        # clean_input is "". We skip processing and ask them to type something.
        if not clean_input:
            print("Bot: (Please type a message.)")
            continue  # Go back to the top of the loop immediately

        # ── Guard 2: Exit Check ────────────────────────────────────────
        # CRITICAL: This check must come BEFORE the knowledge base lookup.
        # If the input is an exit command, print farewell and break the loop.
        # 'break' exits the while loop entirely — clean, controlled termination.
        if clean_input in EXIT_COMMANDS:
            print(f"Bot: Goodbye! Thanks for chatting with {BOT_NAME}. Session ended.")
            break  # This is the ONLY valid exit path from this loop.

        # ── Step 3: Get Response ───────────────────────────────────────
        # Delegate to the pure logic function. O(1) dictionary lookup.
        response = get_response(clean_input)

        # ── Step 4: Print Response ─────────────────────────────────────
        print(f"Bot: {response}")
        print()  # Blank line for readability between turns

    # Loop has ended (break was called). Program terminates normally here.
```

---

## Phase 5: Entrypoint & Error Handling

```python
# ── SECTION 5: ENTRYPOINT ─────────────────────────────────────────────────────

if __name__ == "__main__":
    # The try/except catches KeyboardInterrupt (Ctrl+C).
    # Without this, pressing Ctrl+C prints a ugly traceback.
    # With this, the user gets a clean farewell message.
    try:
        run_chatbot()
    except KeyboardInterrupt:
        # \n moves to a new line (Ctrl+C may leave cursor mid-line)
        print(f"\nBot: Session interrupted. Goodbye!")
```

**Why `if __name__ == "__main__"`?**  
This block only runs when you execute `python chatbot.py` directly. If another file imports `chatbot.py` (e.g., a test file importing `get_response`), the chatbot loop does NOT start automatically.

---

## Phase 6: Complete Working File

Putting it all together — your complete `chatbot.py`:

```python
"""
chatbot.py
──────────
Project 1: Rule-Based AI Chatbot
DecodeLabs Industrial Training Kit | Batch 2026
Author: [Your Name] | Date: [Date]
"""

# ── SECTION 1: CONFIGURATION ──────────────────────────────────────────────────

BOT_NAME = "DecodesBot"

EXIT_COMMANDS = frozenset({"quit", "exit"})

FALLBACK_RESPONSE = (
    "I don't understand that yet. "
    "Type 'help' to see what I can do."
)

# ── SECTION 2: KNOWLEDGE BASE ─────────────────────────────────────────────────

KNOWLEDGE_BASE = {
    "hello":         "Hello! How can I help you today?",
    "hi":            "Hey there! What can I do for you?",
    "hey":           "Hi! Ask me anything.",
    "how are you":   "All systems running perfectly — I'm deterministic, after all!",
    "who are you":   f"I am {BOT_NAME}, a rule-based AI at DecodeLabs.",
    "what is your name": f"My name is {BOT_NAME}.",
    "what is ai":    "AI is the simulation of human intelligence by machines.",
    "what is machine learning": "ML is a subset of AI where systems learn from data.",
    "what is a chatbot": "A chatbot is software that simulates human conversation.",
    "what is a rule based system": "A rule-based system uses predefined logic — deterministic and traceable.",
    "help":          "I know: hello, how are you, who are you, what is ai, what is machine learning, help. Type 'quit' to exit.",
    "what can you do": "I can answer AI basics. Type 'help' for the full list.",
    "thanks":        "You're welcome!",
    "thank you":     "Happy to help!",
    "bye":           "Goodbye! (Type 'quit' to actually exit.)",
    "goodbye":       "See you! (Type 'quit' to end the session.)",
}

# ── SECTION 3: CORE LOGIC ─────────────────────────────────────────────────────

def get_response(clean_input: str) -> str:
    """Return the response for a normalized input string. O(1) lookup."""
    return KNOWLEDGE_BASE.get(clean_input, FALLBACK_RESPONSE)

# ── SECTION 4: RUNTIME ────────────────────────────────────────────────────────

def run_chatbot() -> None:
    """Run the main chatbot loop."""
    print("=" * 50)
    print(f"  {BOT_NAME} — Rule-Based AI Chatbot")
    print(f"  Type 'help' | Type 'quit' to exit")
    print("=" * 50 + "\n")

    while True:
        raw_input = input("You: ")
        clean_input = raw_input.strip().lower()

        if not clean_input:
            print("Bot: (Please type a message.)\n")
            continue

        if clean_input in EXIT_COMMANDS:
            print(f"Bot: Goodbye! Session ended.\n")
            break

        response = get_response(clean_input)
        print(f"Bot: {response}\n")

# ── SECTION 5: ENTRYPOINT ─────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        run_chatbot()
    except KeyboardInterrupt:
        print("\nBot: Session interrupted. Goodbye!")
```

---

## Phase 7: README.md

Your submission must include a README. Here's a template:

```markdown
# DecodesBot — Rule-Based AI Chatbot
**DecodeLabs Industrial Training Kit | Batch 2026 | Project 1**

## What This Is
A deterministic rule-based chatbot built in Python using dictionary-based
intent matching. This is the foundation project for the AI track at DecodeLabs.

## How to Run
```bash
python chatbot.py
```

## Requirements
- Python 3.8 or higher
- No external dependencies

## Usage
Type a message and press Enter. The bot responds based on predefined rules.

Available commands:
- `hello`, `hi`, `hey` — greetings
- `how are you` — status
- `who are you` — identity
- `what is ai` — AI definition
- `what is machine learning` — ML definition
- `help` — list all commands
- `quit` / `exit` — end the session

## Architecture
Input → Sanitization (strip + lower) → Dictionary Lookup (O(1)) → Response

## Known Limitations
- Exact string matching only (punctuation matters: "what is ai?" won't match "what is ai")
- Single-turn only (no conversation memory)
- No semantic understanding
```

---

## Common Mistakes to Avoid

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Using `if-elif` for KB dispatch | O(n) complexity; violates architecture | Use `dict.get()` |
| Checking exit AFTER KB lookup | Exit command gets a chat response instead of exiting | Check exit BEFORE KB |
| Not calling `.strip()` | `" hello"` won't match `"hello"` | Always strip first |
| Not calling `.lower()` | `"Hello"` won't match `"hello"` | Always lowercase |
| `sys.exit()` instead of `break` | Abrupt termination; not loop-controlled | Use `break` |
| Empty fallback string | Silent failure on unknown input | Always set a non-empty fallback |
| Checking empty string last | Wasted lookup before guard | Check `not clean_input` first |
| Putting exit keywords in KB | Exit could return a response instead of exiting | Keep EXIT_COMMANDS separate |

---

*See `TEST_PLAN.md` for the test cases you need to verify before submitting.*
