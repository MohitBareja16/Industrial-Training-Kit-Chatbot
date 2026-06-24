# Product Requirements Document (PRD)
## Project 1: Rule-Based AI Chatbot
**Organization:** DecodeLabs  
**Batch:** 2026  
**Track:** Artificial Intelligence — Foundation Phase  
**Document Version:** 1.0  
**Status:** Approved for Development  

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Success Criteria](#3-goals--success-criteria)
4. [Scope](#4-scope)
5. [User Personas](#5-user-personas)
6. [Functional Requirements](#6-functional-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [System Architecture](#8-system-architecture)
9. [Data Design](#9-data-design)
10. [Control Flow Specification](#10-control-flow-specification)
11. [Error Handling & Edge Cases](#11-error-handling--edge-cases)
12. [Acceptance Criteria & Testing](#12-acceptance-criteria--testing)
13. [Constraints & Assumptions](#13-constraints--assumptions)
14. [Out of Scope](#14-out-of-scope)
15. [Risks & Mitigations](#15-risks--mitigations)
16. [Glossary](#16-glossary)
17. [PRD Self-Audit](#17-prd-self-audit)

---

## 1. Executive Summary

This document defines the complete requirements for **Project 1: Rule-Based AI Chatbot**, the mandatory foundation milestone for all DecodeLabs 2026 AI interns. The project requires building a deterministic, rule-driven chatbot in Python that operates as a continuous interactive loop. It uses a dictionary-based knowledge base (hash map) for O(1) response lookup, explicit input sanitization, a clean exit mechanism, and a graceful fallback for unrecognized inputs.

The core pedagogical objective is to demonstrate mastery of **Control Flow** and **Logic** before progressing to probabilistic/ML-based systems. The chatbot is a "white box" — every input-to-output path is fully traceable, with zero hallucination risk.

Completion of this project is the prerequisite gate to unlock all subsequent projects in the internship track.

---

## 2. Problem Statement

Before an AI engineer can work with probabilistic systems (LLMs, neural networks), they must prove they can construct a **deterministic logic engine** — a system where every output is 100% predictable, auditable, and explainable. This foundational skill directly maps to the real-world practice of building **AI guardrails** (e.g., NVIDIA NeMo, Llama Guard) that act as the rule-based control layer sitting above LLM probabilistic cores.

The problem: interns begin training with conceptual AI knowledge but no hands-on experience building a controlled, looping, stateful interaction system from scratch.

The solution: build a rule-based chatbot that exercises every key primitive — loops, conditionals, dictionaries, input sanitization, and fallback logic — in one cohesive program.

---

## 3. Goals & Success Criteria

### 3.1 Primary Goals
| ID | Goal | Measurable Outcome |
|----|------|--------------------|
| G-01 | Demonstrate control flow mastery | Program runs without infinite hang or crash |
| G-02 | Implement O(1) intent lookup | Dictionary `.get()` used; no bare if-elif chains for response routing |
| G-03 | Handle all input variations gracefully | Mixed case, leading/trailing whitespace, empty input — all handled |
| G-04 | Support clean program termination | Exit command breaks the loop without error or exception |
| G-05 | Produce a quality-verified submission | Code reviewed and passes all acceptance criteria in §12 |

### 3.2 Success Criteria (Binary Pass/Fail)
- [ ] Program starts and immediately enters the input loop
- [ ] At least 5 distinct intents are handled in the knowledge base
- [ ] Input is lowercased and stripped before matching
- [ ] An unrecognized input returns the fallback response (never crashes)
- [ ] Typing `quit` (or equivalent) exits the loop cleanly
- [ ] No bare `if-elif` ladder is used for the core response dispatch
- [ ] Code is readable with comments explaining each logical section

---

## 4. Scope

### 4.1 In Scope
- A single Python script (`chatbot.py`)
- A `while True` input loop
- Input sanitization (`.lower().strip()`)
- A dictionary-based knowledge base with a minimum of 5 intents
- A `.get()` fallback response for unrecognized inputs
- An exit/quit command that breaks the loop
- Inline code comments per the documentation standard
- A `README.md` in the project root

### 4.2 Out of Scope
_(See §14 for full detail)_
- Machine learning or NLP-based intent classification
- Persistent memory / conversation history
- Multi-turn dialogue context
- Web UI, GUI, or API interface
- External libraries beyond Python's standard library
- User authentication or session management
- Logging to external files (optional stretch only)

---

## 5. User Personas

### Persona A — The Intern (Primary User)
- **Who:** A student/early-career developer enrolled in DecodeLabs 2026 batch
- **Goal:** Complete Project 1 to unlock subsequent projects and build their portfolio
- **Technical Level:** Knows Python basics (variables, loops, functions); unfamiliar with AI system architecture
- **Pain Points:** May confuse `if-elif` ladders with professional patterns; may not understand why sanitization matters
- **Need:** Clear spec to implement against; understands *why* each component exists

### Persona B — The Reviewer (Secondary User)
- **Who:** DecodeLabs mentor/evaluator running the submitted chatbot
- **Goal:** Verify the submission meets quality standards in under 5 minutes
- **Technical Level:** Senior engineer, fluent in Python
- **Need:** Predictable behavior, readable code, all acceptance criteria demonstrably met

### Persona C — The End User (Tertiary)
- **Who:** Anyone typing into the chatbot's terminal interface
- **Goal:** Get a response to their input
- **Need:** The system never crashes regardless of what is typed

---

## 6. Functional Requirements

Requirements are tagged: **MUST** (mandatory), **SHOULD** (strongly recommended), **MAY** (optional/stretch).

---

### FR-01 — Continuous Input Loop  
**Priority:** MUST  
**Description:** The chatbot shall run in an infinite `while True` loop. Each iteration shall prompt the user for input, process it, print a response, and return to the top of the loop. The loop shall only terminate via the exit command (FR-05).  
**Rationale:** This models the "heartbeat" of any interactive AI system — a persistent event loop.

```
LOOP INVARIANT:
  PRE:  Program has started successfully
  POST: Program is waiting for user input OR has exited cleanly
  BODY: One full IPO cycle (Input → Process → Output) per iteration
```

---

### FR-02 — Input Sanitization  
**Priority:** MUST  
**Description:** All raw user input SHALL be processed through normalization before any matching occurs.

**Required transformations (in order):**
1. `.strip()` — remove leading and trailing whitespace
2. `.lower()` — convert all characters to lowercase

**Implementation:**
```python
raw_input = input("You: ")
clean_input = raw_input.strip().lower()
```

**Rationale:** "Hello", "  hello  ", "HELLO", and "HeLLo " must all resolve to the same intent. Without sanitization, the knowledge base would require exponential key duplication.

**Edge Cases Handled:**
- All-caps input → normalized
- Extra spaces → stripped
- Mixed case → normalized
- Tab characters at start/end → stripped

---

### FR-03 — Knowledge Base (Dictionary)  
**Priority:** MUST  
**Description:** All chatbot responses SHALL be stored in a Python dictionary. The keys are normalized intent strings; the values are response strings. The knowledge base shall contain a **minimum of 5 intent-response pairs** (excluding the exit command).

**Required Intent Categories (minimum coverage):**

| Intent Key(s) | Category | Example Response |
|--------------|----------|-----------------|
| `hello`, `hi`, `hey` | Greeting | "Hello! How can I help you today?" |
| `bye`, `goodbye` | Farewell | "Goodbye! Have a great day." |
| `how are you` | Status query | "I'm just a bot, but I'm running perfectly!" |
| `what is ai` | Knowledge query | "AI is the simulation of human intelligence by machines." |
| `help` | Assistance | "I can answer questions. Try: hello, what is ai, help." |
| `name`, `who are you` | Identity | "I am DecodesBot, your rule-based AI assistant." |

> Note: A single key maps to a single response. Multiple keys for the same intent are separate entries (by design — see §9 for advanced multi-key pattern).

**Prohibition:** The knowledge base dictionary SHALL NOT be used to store the exit command. Exit logic is handled separately (FR-05).

---

### FR-04 — Response Dispatch via `.get()`  
**Priority:** MUST  
**Description:** The chatbot SHALL use the dictionary `.get()` method for all response lookups. This provides O(1) lookup performance and an atomic lookup-with-fallback in a single operation.

**Implementation:**
```python
fallback = "I don't understand that. Type 'help' for available commands."
response = responses.get(clean_input, fallback)
```

**Prohibition:** A bare `if-elif` ladder SHALL NOT be the primary dispatch mechanism for the knowledge base. This is explicitly classified as the "Anti-Pattern" (IF-ELIF Ladder) in the project architecture brief.

**Why `.get()` over `if key in dict`:**
- `.get(key, default)` is a single atomic operation
- `if key in dict: return dict[key]; else: return fallback` is two operations
- `.get()` is the idiomatic Python pattern and avoids a race-condition-like dual-access

---

### FR-05 — Exit Strategy  
**Priority:** MUST  
**Description:** The chatbot SHALL support a clean exit command. When the user types a recognized exit keyword, the system SHALL print a farewell message and `break` out of the `while True` loop, terminating the program gracefully.

**Required exit keywords (minimum):** `quit`, `exit`  
**Recommended additions:** `bye`, `goodbye` (may overlap with FR-03 — see §11 for resolution)

**Implementation pattern:**
```python
EXIT_COMMANDS = {"quit", "exit", "bye", "goodbye"}

if clean_input in EXIT_COMMANDS:
    print("Bot: Goodbye! Session ended.")
    break
```

**Constraint:** The exit check SHALL occur BEFORE the knowledge base lookup in each loop iteration (see §10 for flow order rationale).

**Prohibition:** The program SHALL NOT exit via `sys.exit()`, `os._exit()`, or raising an uncaught exception. Only `break` is permitted.

---

### FR-06 — Fallback Response  
**Priority:** MUST  
**Description:** For any input that does not match a knowledge base key AND is not an exit command, the chatbot SHALL return a defined fallback/default response. This response SHALL never be an empty string.

**Recommended fallback:** `"I don't understand that yet. Type 'help' for a list of things I know."`

**Rationale:** The fallback is the safety net that guarantees the system never produces an empty or error output. In production AI systems, this is the equivalent of the guardrail's default-deny policy.

---

### FR-07 — Empty Input Handling  
**Priority:** MUST  
**Description:** If the user presses Enter without typing anything, `clean_input` will be an empty string `""`. The chatbot SHALL handle this gracefully — either via a dedicated empty-string key in the knowledge base, or by checking for it before dispatch.

**Recommended pattern:**
```python
if not clean_input:
    print("Bot: Please type something!")
    continue
```

**Rationale:** Empty input is the most common accidental input. Without this guard, the fallback message would appear on every blank Enter press, which is poor UX.

---

### FR-08 — Output Format  
**Priority:** SHOULD  
**Description:** All chatbot responses SHALL be printed with a `Bot:` prefix for clarity. The user prompt SHALL use `You: ` (with a trailing space).

```
You: hello
Bot: Hello! How can I help you today?
```

**Rationale:** Consistent labeling makes the conversation log readable and mirrors real chat interfaces.

---

### FR-09 — Startup Banner  
**Priority:** SHOULD  
**Description:** On launch, the chatbot SHOULD print a startup banner that identifies the bot and provides basic usage instructions, including how to exit.

**Example:**
```
========================================
  DecodesBot — Rule-Based AI Chatbot
  Type 'help' for commands.
  Type 'quit' to exit.
========================================
```

---

### FR-10 — Modular Function Structure  
**Priority:** SHOULD  
**Description:** The program SHOULD be organized into at least two named functions:
- `get_response(user_input: str) -> str` — pure function, takes clean input, returns response string
- `run_chatbot() -> None` — contains the loop, I/O, and orchestration

**Rationale:** Separation of concerns. The `get_response` function becomes independently testable. This mirrors professional architecture where the logic engine is decoupled from the I/O layer.

---

## 7. Non-Functional Requirements

### NFR-01 — Performance
- Response lookup must complete in O(1) time (enforced by dictionary usage — FR-04)
- No response shall take more than 1ms to compute on any modern machine (rule-based, no network calls)

### NFR-02 — Reliability
- The program SHALL NOT crash on any valid string input
- The program SHALL NOT crash on empty input
- The only termination path is the explicit exit command (FR-05)

### NFR-03 — Readability
- Code SHALL include section-level comments (e.g., `# --- KNOWLEDGE BASE ---`)
- All variables SHALL use descriptive snake_case names
- No magic strings without assignment to a named constant

### NFR-04 — Portability
- The program SHALL run on Python 3.8+ with zero external dependencies
- No third-party libraries (`pip install`) are required or permitted

### NFR-05 — Testability
- The `get_response()` function (FR-10) SHALL be importable and callable independently from the main loop, enabling unit testing without launching the interactive session

### NFR-06 — Maintainability
- Adding a new intent MUST only require adding one line to the knowledge base dictionary
- No other part of the code should need modification to add a new simple intent

---

## 8. System Architecture

### 8.1 IPO Model (Input → Process → Output)

```
┌─────────────────────────────────────────────────────────────┐
│                        CHATBOT SYSTEM                        │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │    INPUT     │───▶│   PROCESS    │───▶│    OUTPUT    │  │
│  │  (Raw Feed)  │    │ (Logic Skel.)│    │ (Feedback    │  │
│  │              │    │              │    │    Loop)     │  │
│  │ Sanitization │    │ Intent Match │    │ Response Gen │  │
│  │ & Normalize  │    │ & State Ctrl │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                              │                               │
│                    ┌─────────▼─────────┐                    │
│                    │   KNOWLEDGE BASE  │                    │
│                    │  (Dictionary/     │                    │
│                    │   Hash Map)       │                    │
│                    └───────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 The White Box Guarantee

This chatbot is a "white box" system:
- **Traceability:** Input → Sanitization → Lookup → Output. Every step is visible in code.
- **Safety:** Zero hallucination risk. Every response is hard-coded.
- **Compliance:** The logic is fully auditable — critical for Finance & Healthcare AI guardrail applications.

### 8.3 Module Structure

```
chatbot.py
│
├── CONSTANTS
│   ├── EXIT_COMMANDS (set)
│   └── FALLBACK_RESPONSE (str)
│
├── KNOWLEDGE_BASE (dict)
│   └── {intent_key: response_string, ...}
│
├── get_response(clean_input: str) -> str
│   ├── Lookup: responses.get(clean_input, FALLBACK)
│   └── Returns: response string
│
└── run_chatbot() -> None
    ├── Print startup banner
    └── while True:
        ├── raw_input = input("You: ")
        ├── clean_input = raw_input.strip().lower()
        ├── [Guard] if not clean_input → continue
        ├── [Guard] if clean_input in EXIT_COMMANDS → print + break
        ├── response = get_response(clean_input)
        └── print(f"Bot: {response}")
```

---

## 9. Data Design

### 9.1 Knowledge Base Schema

```python
KNOWLEDGE_BASE: dict[str, str] = {
    # Key: normalized (lowercased, stripped) user input string
    # Value: exact response string to display
    
    "hello":        "Hello! How can I help you today?",
    "hi":           "Hey there! What can I do for you?",
    "hey":          "Hi! Ask me anything.",
    "how are you":  "I'm just a bot, but all systems are running perfectly!",
    "what is ai":   "AI is the simulation of human intelligence processes by machines.",
    "what can you do": "I can answer basic questions. Type 'help' to see what I know.",
    "help":         "Available commands: hello, how are you, what is ai, help, quit.",
    "name":         "I'm DecodesBot — a rule-based AI built on pure logic.",
    "who are you":  "I am DecodesBot, your deterministic AI assistant at DecodeLabs.",
    "thanks":       "You're welcome! Is there anything else?",
    "thank you":    "Happy to help! Anything else you'd like to know?",
}
```

### 9.2 Key Design Rules
- All keys MUST be lowercase (sanitization ensures input is lowercased before lookup)
- All keys MUST be stripped (no leading/trailing spaces in keys)
- Keys MUST be exact-match strings (no regex, no wildcards — this is Project 1)
- Values MUST be non-empty strings
- The dictionary MUST NOT contain the exit commands as keys

### 9.3 Exit Commands Set

```python
EXIT_COMMANDS: frozenset[str] = frozenset({"quit", "exit"})
```

Using a `frozenset` (or `set`) ensures O(1) membership testing (`in` operator) — consistent with the hash map philosophy.

> **Design Decision:** `bye` and `goodbye` are intentionally kept in the KNOWLEDGE_BASE (not EXIT_COMMANDS) by default. This means typing `bye` gives a friendly farewell response but does NOT exit the program. Only `quit` and `exit` terminate. This is a deliberate UX and architecture choice — document it in your code comments. Interns may choose to move them to EXIT_COMMANDS but must note the trade-off.

---

## 10. Control Flow Specification

### 10.1 Complete Execution Flow

```
START
  │
  ▼
Print Startup Banner
  │
  ▼
┌─────────────────────────────────────────┐
│             MAIN LOOP (while True)      │
│                                         │
│  raw = input("You: ")                   │
│  clean = raw.strip().lower()            │
│            │                            │
│            ▼                            │
│     [GUARD-1] clean == ""?              │
│         YES ──▶ print hint, CONTINUE   │
│         NO  ──▶ proceed                │
│            │                            │
│            ▼                            │
│     [GUARD-2] clean in EXIT_COMMANDS?  │
│         YES ──▶ print farewell, BREAK  │
│         NO  ──▶ proceed                │
│            │                            │
│            ▼                            │
│     response = get_response(clean)      │
│     (dict.get with fallback)            │
│            │                            │
│            ▼                            │
│     print(f"Bot: {response}")           │
│            │                            │
│            └──────────────── LOOP ──┘  │
└─────────────────────────────────────────┘
  │
  ▼ (after break)
END
```

### 10.2 Guard Order Rationale

Guards MUST be evaluated in this exact order:
1. **Empty check first** — prevents needless dictionary lookup on empty string
2. **Exit check second** — critical path; must be checked before any response generation
3. **Knowledge lookup last** — only reached if input is non-empty and non-exit

Reversing guards 1 and 2 is functionally acceptable but semantically wrong (exit command `""` does not exist, so it's a micro-optimization to check empty first). Placing knowledge lookup before exit is a **bug** — exit would never trigger.

---

## 11. Error Handling & Edge Cases

| Input | After Sanitization | Expected Behavior | Handled By |
|-------|--------------------|-------------------|------------|
| `""` (empty Enter) | `""` | Print hint, continue loop | FR-07 / GUARD-1 |
| `"   "` (spaces only) | `""` | Same as above | `.strip()` + GUARD-1 |
| `"\t\n"` (whitespace) | `""` | Same as above | `.strip()` + GUARD-1 |
| `"HELLO"` | `"hello"` | Matched in KB | `.lower()` |
| `"  Hello  "` | `"hello"` | Matched in KB | `.strip().lower()` |
| `"quit"` | `"quit"` | Exit cleanly | GUARD-2 |
| `"QUIT"` | `"quit"` | Exit cleanly | `.lower()` + GUARD-2 |
| `"xyz123"` | `"xyz123"` | Fallback response | `.get()` default |
| `"hello world"` | `"hello world"` | Fallback (no exact match) | `.get()` default |
| `"what is ai?"` | `"what is ai?"` | Fallback (punctuation!) | Note: see §11.1 |
| `KeyboardInterrupt` (Ctrl+C) | N/A | Graceful exit message | See §11.2 |

### 11.1 Punctuation Edge Case
The current design uses exact string matching. `"what is ai?"` will NOT match `"what is ai"`. This is a known limitation of Project 1 (exact-match / discrete mapping). It is acceptable and expected. Interns SHOULD document this limitation. Solving it (regex, token matching) is a stretch goal only.

### 11.2 KeyboardInterrupt Handling (SHOULD)
Wrapping the main loop in a `try/except KeyboardInterrupt` is strongly recommended:

```python
try:
    run_chatbot()
except KeyboardInterrupt:
    print("\nBot: Session interrupted. Goodbye!")
```

This prevents an ugly traceback if the user presses Ctrl+C.

---

## 12. Acceptance Criteria & Testing

### 12.1 Manual Test Cases

Every test case must PASS for the submission to be accepted.

| TC-ID | Input Sequence | Expected Output | Pass/Fail |
|-------|---------------|-----------------|-----------|
| TC-01 | `hello` | `Bot: Hello! How can I help you today?` | |
| TC-02 | `HELLO` | Same as TC-01 | |
| TC-03 | `  hello  ` | Same as TC-01 | |
| TC-04 | `HeLLo` | Same as TC-01 | |
| TC-05 | *(empty Enter)* | Hint message, loop continues | |
| TC-06 | `   ` *(spaces)* | Hint message, loop continues | |
| TC-07 | `xyzunknown` | Fallback response | |
| TC-08 | `quit` | Farewell + program exits | |
| TC-09 | `QUIT` | Same as TC-08 | |
| TC-10 | `exit` | Farewell + program exits | |
| TC-11 | `help` | Lists available commands | |
| TC-12 | `what is ai` | AI definition response | |
| TC-13 | `how are you` | Status response | |
| TC-14 | *(Ctrl+C)* | Graceful message, no traceback | |
| TC-15 | 10 consecutive unknowns | 10 fallback responses; no crash | |

### 12.2 Code Review Checklist

| Check | Requirement | Verified |
|-------|-------------|----------|
| CR-01 | `while True:` loop present | |
| CR-02 | `.strip().lower()` applied to all input | |
| CR-03 | Knowledge base is a `dict` with ≥5 entries | |
| CR-04 | `.get()` used for dispatch (no bare if-elif for KB lookup) | |
| CR-05 | Exit check uses `break` | |
| CR-06 | Fallback response is a non-empty string | |
| CR-07 | Empty input is handled (no silent pass) | |
| CR-08 | Code has section comments | |
| CR-09 | `get_response()` is a separate function | |
| CR-10 | No external library imports | |

---

## 13. Constraints & Assumptions

### Constraints
- **Language:** Python 3.8 or higher
- **Dependencies:** Zero external packages. Standard library only.
- **Interface:** Terminal/CLI only
- **Pattern:** Dictionary `.get()` for dispatch — `if-elif` ladder is explicitly prohibited for the core dispatch
- **Submission:** Single `.py` file + `README.md`

### Assumptions
- The intern has a working Python 3 installation
- The intern is comfortable with basic Python: variables, loops, dictionaries, functions, f-strings
- The runtime environment is a standard terminal (bash, zsh, PowerShell, cmd)
- No persistent storage is needed (stateless per session)

---

## 14. Out of Scope

The following are explicitly excluded from Project 1. They may appear in future projects.

| Feature | Reason Out of Scope |
|---------|---------------------|
| NLP / fuzzy matching | Requires ML/NLP libraries — Project 2+ |
| Conversation memory | Stateful multi-turn context — future project |
| Regex-based matching | Adds complexity beyond P1 objectives |
| Web or GUI interface | CLI only for P1 |
| File-based logging | Optional stretch; not graded |
| External APIs | No network calls — P1 is fully self-contained |
| Unit test files | Encouraged but not graded in P1 |
| Database for responses | Dictionary is sufficient; DB is over-engineering for P1 |
| Async/concurrent input | Single-threaded blocking I/O only |

---

## 15. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Intern uses if-elif ladder instead of dict | High | Medium | Explicit prohibition in FR-04; architecture diagram included |
| Exit command never triggers (placed after KB lookup) | Medium | High | Guard order specified in §10.2; test TC-08 catches this |
| Empty input causes crash or silent loop | Medium | Medium | FR-07 and GUARD-1 explicitly required |
| Punctuation breaks exact matching | High | Low | Documented as known limitation in §11.1 |
| `sys.exit()` used instead of `break` | Low | Medium | Prohibition in FR-05 |
| Intern overlaps `bye` in both KB and EXIT_COMMANDS | Medium | Low | Design decision documented in §9.3 |
| KeyboardInterrupt produces ugly traceback | Medium | Low | NFR-02 + §11.2 SHOULD requirement |

---

## 16. Glossary

| Term | Definition |
|------|-----------|
| **Deterministic** | A system where the same input always produces the same output. No randomness. |
| **Probabilistic** | A system (like an LLM) where the same input may produce different outputs. |
| **White Box** | A system whose internal logic is fully visible and traceable (opposite of Black Box). |
| **O(1)** | Constant time complexity — execution time does not grow with the size of the data. |
| **O(n)** | Linear time complexity — execution time grows proportionally with data size. |
| **Sanitization** | Normalizing raw input to remove inconsistencies (case, whitespace) before processing. |
| **Intent** | The semantic category of user input (e.g., "greeting", "knowledge query"). |
| **Fallback** | The default response returned when no intent is matched. |
| **Hash Map** | A data structure (Python `dict`) that maps keys to values with O(1) average lookup. |
| **Guardrail** | A rule-based system layer that controls/filters inputs or outputs to/from an LLM. |
| **IPO Model** | Input → Process → Output. The foundational model of a computational system. |
| **EXIT_COMMANDS** | The set of strings that trigger program termination. |
| **Knowledge Base** | The dictionary of all defined intent→response pairs. |
| **GUARD** | A conditional check at the top of the loop before the main dispatch logic. |

---

## 17. PRD Self-Audit

*This section audits the PRD for loopholes, ambiguities, and gaps before development begins.*

### 17.1 Completeness Audit

| Area | Covered? | Notes |
|------|---------|-------|
| What the program must do | ✅ | FR-01 through FR-10 |
| What the program must NOT do | ✅ | Prohibitions in FR-04, FR-05; §14 Out of Scope |
| How inputs are processed | ✅ | FR-02, §10 |
| How outputs are generated | ✅ | FR-04, FR-06, FR-08 |
| All edge cases | ✅ | §11, TC-01 through TC-15 |
| Performance requirements | ✅ | NFR-01, O(1) enforced by FR-04 |
| Error handling | ✅ | FR-07, §11.2 |
| Testability | ✅ | §12, FR-10 |
| Architecture | ✅ | §8 |
| Data design | ✅ | §9 |

### 17.2 Identified Loopholes & Resolutions

| # | Loophole | Resolution |
|---|---------|-----------|
| L-01 | **`bye` ambiguity**: Is `bye` an exit command or a KB response? If in both, which wins? | §9.3 explicitly resolves: `bye` is in KB by default (farewell response). Only `quit`/`exit` terminate. Guard order in §10.2 means EXIT check runs before KB lookup — so if intern moves `bye` to EXIT_COMMANDS, it exits. Documented design decision. |
| L-02 | **Minimum 5 intents**: Does `quit`/`exit` count toward the 5? | FR-03 explicitly states: "minimum of 5 intent-response pairs (excluding the exit command)." Exit commands are a separate construct (FR-05). |
| L-03 | **`if-elif` prohibition**: Could an intern use `if-elif` to check KB AND still use `.get()`? | FR-04 states `.get()` SHALL be used. Using `if-elif` inside `get_response()` to route to different handlers is still prohibited. The KB lookup must be the `.get()` call. |
| L-04 | **`sys.exit()` loophole**: Intern could use `sys.exit()` and it would still "work." | FR-05 explicitly prohibits `sys.exit()` and states only `break` is permitted. CR-05 verifies this. |
| L-05 | **Empty fallback string**: Could the fallback be `""`? | FR-06 explicitly states the fallback SHALL NEVER be an empty string. |
| L-06 | **Punctuation mismatch not caught by tests**: TC tests don't cover `"what is ai?"`. | §11.1 documents this as a known limitation, not a bug. It is out of scope for P1. |
| L-07 | **Function requirement wording**: FR-10 says "SHOULD" not "MUST" — could be skipped. | Correct — it's SHOULD (strongly recommended). CR-09 is still on the code review checklist, meaning reviewers check for it. Interns who skip it are noted but not failed solely on this. |
| L-08 | **Multiple keys same response**: Is it acceptable to have `"hello"` and `"hi"` both map to the same response string? | Yes, this is explicitly shown in §9.1. It is valid and expected. |
| L-09 | **Knowledge base mutation during runtime**: What if the intern modifies the dict inside the loop? | Not explicitly prohibited, but NFR-06 states adding an intent should only require one line. If the intern implements dynamic learning (adding to dict at runtime), that is an advanced stretch feature — acceptable but must not break the mandatory requirements. |
| L-10 | **`input()` can raise `EOFError`**: In non-interactive mode (piped input), `input()` raises `EOFError` at end of stream. | Added to stretch goals / §11.2 spirit. For interactive P1 use, this is out of scope. Documented as known edge case. |

### 17.3 Ambiguity Resolutions Summary

- "At least 5 intents" = 5 KB entries excluding exit keywords
- "Clean exit" = `break` only, with a printed farewell message
- "No if-elif ladder" = the KB dispatch must use `.get()`, not chained conditionals
- "Sanitization" = `.strip().lower()` in that order (strip first, then lower is fine either order technically, but strip first is the documented pattern)
- "The bot should not crash" = covers all string inputs; `EOFError` is out of scope for P1

---

*Document ends. Proceed to `ARCHITECTURE.md` for the detailed technical architecture.*
