# TEST_PLAN.md
## Project 1: Rule-Based AI Chatbot — Test Specification
**DecodeLabs 2026 | Quality Verification Document**

---

## Overview

All test cases in this plan must pass before a submission is accepted. The test plan is organized into:
1. **Functional Tests** — Does it do what it's supposed to?
2. **Edge Case Tests** — Does it handle unexpected inputs without crashing?
3. **Negative Tests** — Does it correctly NOT do prohibited things?
4. **Code Review Checklist** — Static analysis of the source code

---

## 1. Functional Tests

Run these manually. Type the input shown, verify the output matches.

### 1.1 Greeting Tests

| TC-ID | Input | Expected Output Contains | Pass? |
|-------|-------|--------------------------|-------|
| TC-F-01 | `hello` | "Hello" or similar greeting | ☐ |
| TC-F-02 | `hi` | Greeting response | ☐ |
| TC-F-03 | `hey` | Greeting response | ☐ |

### 1.2 Knowledge Tests

| TC-ID | Input | Expected Output Contains | Pass? |
|-------|-------|--------------------------|-------|
| TC-F-04 | `what is ai` | AI definition | ☐ |
| TC-F-05 | `how are you` | Status/wellbeing response | ☐ |
| TC-F-06 | `who are you` | Bot identity/name | ☐ |
| TC-F-07 | `help` | List of available commands | ☐ |

### 1.3 Exit Tests

| TC-ID | Input | Expected Behavior | Pass? |
|-------|-------|-------------------|-------|
| TC-F-08 | `quit` | Farewell message printed; program ends | ☐ |
| TC-F-09 | `exit` | Farewell message printed; program ends | ☐ |

---

## 2. Sanitization Tests

These verify the sanitization pipeline (strip + lower) works correctly.

| TC-ID | Input | Expected Behavior | Tests What |
|-------|-------|-------------------|-----------|
| TC-S-01 | `HELLO` | Same response as `hello` | `.lower()` |
| TC-S-02 | `Hello` | Same response as `hello` | `.lower()` |
| TC-S-03 | `HeLLo` | Same response as `hello` | `.lower()` |
| TC-S-04 | `  hello  ` | Same response as `hello` | `.strip()` |
| TC-S-05 | `  HELLO  ` | Same response as `hello` | `.strip()` + `.lower()` |
| TC-S-06 | `QUIT` | Program exits cleanly | `.lower()` on exit cmd |
| TC-S-07 | `  quit  ` | Program exits cleanly | `.strip()` on exit cmd |
| TC-S-08 | `EXIT` | Program exits cleanly | `.lower()` on exit cmd |
| TC-S-09 | `WHAT IS AI` | AI definition response | Multi-word lowercase |

**How to test:** Run the bot and type each input. Verify it behaves identically to the lowercase version.

---

## 3. Edge Case Tests

These verify the bot handles unusual or empty inputs gracefully.

| TC-ID | Input Method | Expected Behavior | Pass? |
|-------|-------------|-------------------|-------|
| TC-E-01 | Press Enter (empty) | Hint message; loop continues; no crash | ☐ |
| TC-E-02 | `   ` (spaces only) | Same as TC-E-01 | ☐ |
| TC-E-03 | `xyzunknown123` | Fallback response; loop continues | ☐ |
| TC-E-04 | `!@#$%` | Fallback response; loop continues | ☐ |
| TC-E-05 | `hello world` (multi-word, not in KB) | Fallback response | ☐ |
| TC-E-06 | `what is ai?` (with punctuation) | Fallback (not a match — known limitation) | ☐ |
| TC-E-07 | 10× consecutive unknowns | 10 fallback responses; no crash | ☐ |
| TC-E-08 | Ctrl+C (KeyboardInterrupt) | Clean exit message; no Python traceback | ☐ |
| TC-E-09 | Very long string (500 chars) | Fallback response; no crash | ☐ |
| TC-E-10 | Numeric input `12345` | Fallback response; no crash | ☐ |

---

## 4. Control Flow Tests

These verify the loop and guard logic are correct.

| TC-ID | Scenario | Expected Behavior | Pass? |
|-------|----------|-------------------|-------|
| TC-CF-01 | Exit command is typed | Loop breaks; program does NOT continue to next turn | ☐ |
| TC-CF-02 | Multiple turns before exit | All turns processed; clean exit on quit | ☐ |
| TC-CF-03 | Empty input followed by valid input | Empty hint; then correct response on next turn | ☐ |
| TC-CF-04 | Unknown input followed by exit | Fallback; then clean exit | ☐ |

---

## 5. Code Review Checklist

This is a static code review — no running required. Read the source file.

### 5.1 Mandatory Requirements (MUST)

| CR-ID | Requirement | Check Method | Pass? |
|-------|-------------|-------------|-------|
| CR-01 | `while True:` loop is present | Search source for `while True` | ☐ |
| CR-02 | Input goes through `.strip().lower()` (or `.lower().strip()`) | Search for both methods on input | ☐ |
| CR-03 | Knowledge base is a `dict` literal or assigned to a variable | Verify type is `dict` | ☐ |
| CR-04 | Knowledge base has ≥ 5 entries (excluding exit keywords) | Count keys | ☐ |
| CR-05 | `.get()` is used for response dispatch | Search for `.get(` in source | ☐ |
| CR-06 | Exit is handled with `break` | Search for `break` in source | ☐ |
| CR-07 | No `sys.exit()` or `os._exit()` in source | Search for these; should not appear | ☐ |
| CR-08 | Fallback response is a non-empty string | Inspect the `.get()` default argument | ☐ |
| CR-09 | Empty input is explicitly handled | Search for `not clean_input` or equivalent | ☐ |
| CR-10 | No `import` of external packages | Check all `import` statements | ☐ |
| CR-11 | Exit check is BEFORE knowledge base lookup in loop | Read loop body top-to-bottom | ☐ |

### 5.2 Strongly Recommended (SHOULD)

| CR-ID | Requirement | Check Method | Pass? |
|-------|-------------|-------------|-------|
| CR-12 | `get_response()` is a separate function | Search for `def get_response` | ☐ |
| CR-13 | `run_chatbot()` or equivalent wraps the loop | Search for function definition | ☐ |
| CR-14 | Code has section-level comments (`# ── SECTION ...`) | Scan for comment headers | ☐ |
| CR-15 | Startup banner is printed before loop | Check before `while True` | ☐ |
| CR-16 | `if __name__ == "__main__":` guard present | Search for this pattern | ☐ |
| CR-17 | `KeyboardInterrupt` is caught | Search for `except KeyboardInterrupt` | ☐ |

### 5.3 Anti-Patterns (Must NOT be present)

| CR-ID | Anti-Pattern | Check | Pass? |
|-------|-------------|-------|-------|
| CR-A1 | If-elif ladder used as primary KB dispatch | No chain of `elif clean_input ==` for KB responses | ☐ |
| CR-A2 | Exit keywords also in knowledge base | EXIT_COMMANDS keys should NOT appear in KNOWLEDGE_BASE | ☐ |
| CR-A3 | `sys.exit()` / `os._exit()` used | Not present in source | ☐ |
| CR-A4 | Empty string as fallback response | `.get()` default is non-empty | ☐ |
| CR-A5 | Knowledge base lookup before exit guard | Loop order: empty check → exit check → KB lookup | ☐ |

---

## 6. Automated Unit Test (Optional/Stretch)

If you have set up `get_response()` as a separate importable function, you can write a basic test file:

```python
# test_chatbot.py
# Run with: python test_chatbot.py

from chatbot import get_response, FALLBACK_RESPONSE

def test(description, got, expected):
    status = "PASS" if got == expected else "FAIL"
    print(f"[{status}] {description}")
    if got != expected:
        print(f"       Expected: {repr(expected)}")
        print(f"       Got:      {repr(got)}")

# ── Test: Known intents return expected responses ──────────────────────────────
test("'hello' returns greeting",     
     got=get_response("hello"), 
     expected="Hello! How can I help you today?")

# ── Test: Unknown input returns fallback ───────────────────────────────────────
test("Unknown input returns fallback",     
     got=get_response("xyzunknown123"), 
     expected=FALLBACK_RESPONSE)

# ── Test: Fallback is not empty ────────────────────────────────────────────────
test("Fallback is non-empty",        
     got=bool(FALLBACK_RESPONSE),    
     expected=True)

# ── Test: Sanitization is the CALLER's responsibility ─────────────────────────
# get_response() should NOT receive unsanitized input.
# (Sanitization happens in run_chatbot() before calling get_response())
# This test documents that behavior:
test("Unsanitized 'HELLO' does NOT match (sanitize before calling)",
     got=get_response("HELLO"),      # Deliberate: uppercase bypasses sanitization
     expected=FALLBACK_RESPONSE)     # Should return fallback (not the hello response)

print("\nAll tests complete.")
```

**Run with:**
```bash
python test_chatbot.py
```

Expected output (all PASS):
```
[PASS] 'hello' returns greeting
[PASS] Unknown input returns fallback
[PASS] Fallback is non-empty
[PASS] Unsanitized 'HELLO' does NOT match (sanitize before calling)

All tests complete.
```

---

## 7. Submission Verification Checklist

Before submitting, confirm all of the following:

```
Pre-Submission Checklist
────────────────────────
☐ chatbot.py runs without errors: python chatbot.py
☐ All TC-F (Functional) tests pass
☐ All TC-S (Sanitization) tests pass  
☐ All TC-E (Edge Case) tests pass (especially TC-E-01 empty input)
☐ All TC-CF (Control Flow) tests pass
☐ All CR (Code Review) MUST checks pass
☐ No CR anti-patterns present
☐ README.md exists with setup instructions
☐ No external libraries imported
☐ Code has comments explaining each section
```

---

*For architecture reference, see `ARCHITECTURE.md`.*  
*For step-by-step build instructions, see `IMPLEMENTATION_GUIDE.md`.*
