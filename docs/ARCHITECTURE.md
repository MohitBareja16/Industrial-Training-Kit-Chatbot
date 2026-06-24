# ARCHITECTURE.md
## Project 1: Rule-Based AI Chatbot — Technical Architecture
**DecodeLabs 2026 | Module 01 — The Logic Engine**

---

## 1. Architectural Philosophy

This chatbot is built on the **"White Box" principle**: every input-to-output path is fully traceable with zero ambiguity. This is the architectural foundation that modern AI guardrail systems (NVIDIA NeMo, Llama Guard) are built upon.

The architecture deliberately uses the simplest possible structures to solve the problem correctly:
- A `dict` (hash map) over `if-elif` chains → O(1) vs O(n)
- `break` over `sys.exit()` → controlled scope termination
- A dedicated `get_response()` function over inline logic → testable, decoupled

---

## 2. The Two Minds of AI — Architectural Context

This project implements **System 2: The Engineer (Deterministic)**:

```
SYSTEM 1: THE ARTIST          SYSTEM 2: THE ENGINEER
(Probabilistic — LLMs)        (Deterministic — This Project)
─────────────────────         ──────────────────────────────
Inputs → weighted sum         Input → exact match → output
→ threshold → output          Every path is traceable
May hallucinate               Zero hallucination risk
Flexible, creative            Rigid, reliable
O(n) parameters               O(1) lookup
```

In the modern hybrid AI stack:
```
USER INPUT
    │
    ▼
┌─────────────────────────────────────┐
│      RULE-BASED GUARDRAILS          │  ◀── You are building THIS layer
│  (Filtering, Redaction, Blocking)   │
└─────────────────┬───────────────────┘
                  │ (unmatched inputs only)
                  ▼
┌─────────────────────────────────────┐
│      LARGE LANGUAGE MODEL           │
│      (Probabilistic Core)           │
└─────────────────────────────────────┘
```

---

## 3. Component Architecture

### 3.1 File Structure

```
project-1/
├── chatbot.py          # Main application file (REQUIRED)
├── README.md           # Setup & usage documentation (REQUIRED)
└── docs/               # Optional: extended documentation
    └── ARCHITECTURE.md
```

### 3.2 Internal Module Structure (`chatbot.py`)

```
chatbot.py
│
├── ── SECTION 1: IMPORTS ──────────────────────────────
│   (none required — stdlib only)
│
├── ── SECTION 2: CONSTANTS ─────────────────────────────
│   EXIT_COMMANDS: frozenset[str]
│   FALLBACK_RESPONSE: str
│   BOT_NAME: str
│
├── ── SECTION 3: KNOWLEDGE BASE ────────────────────────
│   KNOWLEDGE_BASE: dict[str, str]
│   (minimum 5 entries, all lowercase keys)
│
├── ── SECTION 4: CORE LOGIC ────────────────────────────
│   get_response(clean_input: str) -> str
│   │   Pure function. No side effects. No I/O.
│   │   Takes: normalized string
│   │   Returns: response string (never None, never empty)
│   └── uses: KNOWLEDGE_BASE.get(clean_input, FALLBACK_RESPONSE)
│
└── ── SECTION 5: RUNTIME / ENTRYPOINT ─────────────────
    run_chatbot() -> None
    │   Impure function. Contains all I/O and loop logic.
    │   Side effects: prints to stdout, reads from stdin
    └── if __name__ == "__main__": run_chatbot()
```

---

## 4. Data Flow Architecture

### 4.1 Per-Iteration Data Flow

```
stdin (raw string)
        │
        ▼
    raw_input = input("You: ")
        │
        ▼
    SANITIZATION PIPELINE
    ┌───────────────────────┐
    │  .strip()             │  "  Hello  " → "Hello"
    │  .lower()             │  "Hello"     → "hello"
    └───────────────────────┘
        │
        ▼
    clean_input (str)
        │
        ├── [GUARD-1] clean_input == "" ?
        │       YES → print hint; continue (→ next iteration)
        │       NO  → proceed
        │
        ├── [GUARD-2] clean_input in EXIT_COMMANDS ?
        │       YES → print farewell; break (→ program end)
        │       NO  → proceed
        │
        ▼
    get_response(clean_input)
        │
        ▼
    KNOWLEDGE_BASE.get(clean_input, FALLBACK_RESPONSE)
        │
        ├── KEY FOUND    → return KNOWLEDGE_BASE[clean_input]
        └── KEY NOT FOUND → return FALLBACK_RESPONSE
        │
        ▼
    response (str)
        │
        ▼
    print(f"Bot: {response}")
        │
        ▼
    stdout (response string)
        │
        └──────────────────────── (loop back to input())
```

---

## 5. Performance Architecture

### 5.1 Why Dictionary over If-Elif

The `if-elif` ladder is classified as an **Anti-Pattern** for this use case:

```
IF-ELIF LADDER — O(n) Linear Complexity
────────────────────────────────────────
if input == "hello":      → check 1
elif input == "hi":       → check 2
elif input == "hey":      → check 3
elif input == "how are you": → check 4
...
elif input == "rule_n":   → check n
else: fallback            → check n+1

With 1000 rules: worst case 1001 comparisons per input.
```

```
DICTIONARY — O(1) Constant Time Complexity
──────────────────────────────────────────
KNOWLEDGE_BASE.get(input, fallback)
        │
        ▼
    hash(input) → memory address → value
    
With 1 rule or 10,000 rules: SAME time. 1 operation.
```

**Benchmark (conceptual):**
```
Rules:   10      100     1,000   10,000
───────────────────────────────────────
if-elif: ~10ns   ~100ns  ~1ms    ~10ms
dict:    ~1ns    ~1ns    ~1ns    ~1ns   ← flat line
```

### 5.2 Space Complexity

The dictionary requires O(k) space where k = number of intents. For Project 1's scale (5-50 intents), this is negligible. The `frozenset` for EXIT_COMMANDS is O(e) where e = number of exit keywords (constant, ~2-5).

---

## 6. The Conceptual Bridge: Project 1 → Project 2

Understanding where P1 architecture leads:

```
PROJECT 1 (This)              PROJECT 2 (Next)
Discrete Mapping              Continuous Mapping
Exact Match                   Semantic Match
─────────────────             ──────────────────

KEY ──────────▶ VALUE         VECTOR ──────────▶ MEANING
(string)        (string)      [0.2, 0.9, 0.4]   (approximate)

Hardcoded Link                Learned/Embedded Link
Rigid Structure               Flexible Architecture
```

The mental model shift: in P1, your "key" is the literal string `"hello"`. In P2+, the key becomes a mathematical vector (embedding) in high-dimensional space, and matching is approximate/semantic rather than exact.

---

## 7. Hybrid Architecture (Conceptual Understanding)

For context, this is how P1's logic engine fits into a production AI system:

```
USER QUESTION
      │
      ▼
 ◇ RULE MATCH? ◇
      │         │
      YES        NO
      │         │
      ▼         ▼
 INSTANT      PASS TO LLM
 RESPONSE     (Flexibility)
 (Speed)
```

Your P1 chatbot implements the left branch entirely. Rule matches → instant deterministic response. The right branch (LLM fallback) is what you'll explore in later projects.

---

## 8. Known Architectural Limitations (P1 by Design)

| Limitation | Impact | Resolution in Future Projects |
|-----------|--------|-------------------------------|
| Exact string matching only | `"what is ai?"` ≠ `"what is ai"` | Regex / NLP tokenization |
| Single-turn only (no memory) | Cannot refer to previous turns | Conversation history / context window |
| No semantic understanding | `"tell me about artificial intelligence"` misses | Vector embeddings / LLM |
| Case+whitespace only normalization | Punctuation, synonyms not handled | NLP preprocessing pipeline |
| Hardcoded responses | Cannot generate novel answers | Generative model integration |

These are not bugs. They are the deliberate constraints of the deterministic architecture. They are the precise reason P2+ projects exist.

---

*For implementation guidance, see `IMPLEMENTATION_GUIDE.md`.*  
*For test specifications, see `TEST_PLAN.md`.*
