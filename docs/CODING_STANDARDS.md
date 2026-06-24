# CODING_STANDARDS.md
## Project 1: Rule-Based AI Chatbot — Code Style & Standards
**DecodeLabs 2026 | Quality Reference**

---

## 1. Python Version & Runtime

- **Minimum:** Python 3.8
- **Recommended:** Python 3.10+
- **No virtual environment required** (zero dependencies)
- **Run command:** `python chatbot.py` or `python3 chatbot.py`

---

## 2. File Structure Standard

Every `chatbot.py` submission must follow this exact section order:

```
Section 1: Module docstring
Section 2: Imports (if any — stdlib only)
Section 3: Constants (BOT_NAME, EXIT_COMMANDS, FALLBACK_RESPONSE)
Section 4: Knowledge Base (KNOWLEDGE_BASE dict)
Section 5: Core logic function (get_response)
Section 6: Runtime function (run_chatbot)
Section 7: Entrypoint (if __name__ == "__main__")
```

---

## 3. Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Constants | UPPER_SNAKE_CASE | `BOT_NAME`, `EXIT_COMMANDS`, `FALLBACK_RESPONSE` |
| Functions | lower_snake_case | `get_response()`, `run_chatbot()` |
| Variables | lower_snake_case | `raw_input`, `clean_input`, `response` |
| Dictionary | UPPER_SNAKE_CASE (it's a constant) | `KNOWLEDGE_BASE` |

---

## 4. Comment Standards

### 4.1 Section Headers
Every logical section must start with a clear separator comment:

```python
# ── SECTION NAME ──────────────────────────────────────────────────────────────
```

### 4.2 Inline Explanation Comments
Explain the *why*, not the *what*. The code already shows *what* — comments should explain *why* a decision was made.

```python
# GOOD: explains the why
clean_input = raw_input.strip().lower()
# .strip() ensures "  hello  " matches "hello" (same intent, different whitespace)
# .lower() ensures "HELLO" matches "hello" (same intent, different case)

# BAD: restates the obvious
clean_input = raw_input.strip().lower()  # strip and lowercase the input
```

### 4.3 Function Docstrings
Every function must have a docstring using this format:

```python
def get_response(clean_input: str) -> str:
    """
    One-line summary of what the function does.

    Longer explanation if needed. Explain the algorithm or design decision.

    Args:
        param_name (type): Description.

    Returns:
        type: Description of return value. State if it can be None/empty.
    """
```

---

## 5. Type Hints

Use type hints on all function signatures. This documents expected types and enables IDE support.

```python
# Required
def get_response(clean_input: str) -> str:
def run_chatbot() -> None:

# Constants with type hints (optional but good practice)
BOT_NAME: str = "DecodesBot"
EXIT_COMMANDS: frozenset[str] = frozenset({"quit", "exit"})
KNOWLEDGE_BASE: dict[str, str] = {...}
```

---

## 6. String Formatting

Use **f-strings** (Python 3.6+) for any string that includes a variable:

```python
# CORRECT
print(f"Bot: {response}")
print(f"  {BOT_NAME} — Rule-Based AI Chatbot")

# AVOID
print("Bot: " + response)          # string concatenation
print("Bot: %s" % response)        # old % formatting
print("Bot: {}".format(response))  # .format() — acceptable but f-strings preferred
```

---

## 7. Long String Handling

For long response strings, use implicit string concatenation inside parentheses rather than line continuation (`\`):

```python
# CORRECT — implicit concatenation
FALLBACK_RESPONSE = (
    "I don't understand that yet. "
    "Type 'help' to see what I can do."
)

# ALSO CORRECT — triple quote
HELP_TEXT = """Here's what I understand:
  • hello / hi / hey   → greeting
  • quit / exit        → end session"""

# AVOID — backslash continuation (fragile)
FALLBACK_RESPONSE = "I don't understand that yet. " \
                    "Type 'help' to see what I can do."
```

---

## 8. What NOT to Import

The following are prohibited in Project 1:

```python
# PROHIBITED
import re          # regex — not needed for P1 exact matching
import nltk        # NLP library — P1 is rule-based only
import openai      # LLM API — P1 is self-contained
import tensorflow  # ML framework — P1 is rule-based only
import torch       # ML framework — P1 is rule-based only
import requests    # HTTP — P1 has no network calls

# ALLOWED (stdlib only, use if genuinely needed)
import sys         # Only if absolutely necessary — prefer not to use
import os          # Only if absolutely necessary
import random      # Allowed for stretch: randomize responses for same intent
```

---

## 9. Prohibited Patterns

### 9.1 The If-Elif Ladder (Anti-Pattern)

```python
# ❌ PROHIBITED — O(n) anti-pattern
if clean_input == "hello":
    response = "Hello!"
elif clean_input == "hi":
    response = "Hey!"
elif clean_input == "how are you":
    response = "I'm good!"
# ... continues for every intent
else:
    response = FALLBACK_RESPONSE

# ✅ CORRECT — O(1) pattern
response = KNOWLEDGE_BASE.get(clean_input, FALLBACK_RESPONSE)
```

### 9.2 sys.exit() Instead of break

```python
# ❌ PROHIBITED
import sys
if clean_input in EXIT_COMMANDS:
    sys.exit(0)

# ✅ CORRECT
if clean_input in EXIT_COMMANDS:
    print("Bot: Goodbye!")
    break
```

### 9.3 Empty Fallback

```python
# ❌ PROHIBITED — silent failure
response = KNOWLEDGE_BASE.get(clean_input, "")

# ✅ CORRECT
response = KNOWLEDGE_BASE.get(clean_input, FALLBACK_RESPONSE)
```

### 9.4 Exit Check After KB Lookup

```python
# ❌ WRONG ORDER — exit command gets a chat response instead of exiting
response = KNOWLEDGE_BASE.get(clean_input, FALLBACK_RESPONSE)
if clean_input in EXIT_COMMANDS:   # too late — already looked up
    break

# ✅ CORRECT ORDER
if clean_input in EXIT_COMMANDS:   # check FIRST
    print("Bot: Goodbye!")
    break
response = KNOWLEDGE_BASE.get(clean_input, FALLBACK_RESPONSE)
```

---

## 10. Line Length & Formatting

- **Max line length:** 100 characters (PEP8 recommends 79, but 100 is acceptable for readability)
- **Indentation:** 4 spaces (never tabs)
- **Blank lines between functions:** 2 blank lines
- **Blank lines between sections:** 1 blank line + section comment

---

## 11. Final Quality Bar

Before submitting, your code should be readable to someone who has never seen it before. Ask yourself:

1. If I came back to this in 3 months, would I understand every line?
2. Can a reviewer understand the architecture just by reading the section comments?
3. Does every function have a docstring?
4. Are all the "why" decisions documented in comments?

If the answer to any is "no" — add more comments.

---

*Code is written once, read many times. Write for the reader, not the machine.*
