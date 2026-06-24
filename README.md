# DecodeLabs — Project 1: Rule-Based AI Chatbot
**Industrial Training Kit | Batch 2026 | AI Track**

---

## Quick Start

```bash
python chatbot.py
```

That's it. No installs. No virtual environments. Pure Python.

---

## What You're Building

A **deterministic rule-based chatbot** — the "Logic Engine" that forms the foundation of all AI systems. Before you build systems that *learn*, you must master systems that *reason*.

This chatbot is a **white box**: every input-to-output path is fully traceable, auditable, and predictable. No hallucinations. No surprises.

---

## Project Documentation

| File | Purpose |
|------|---------|
| [`docs/PRD.md`](docs/PRD.md) | Full Product Requirements Document — the authoritative spec |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Technical architecture, data flow, component design |
| [`docs/IMPLEMENTATION_GUIDE.md`](docs/IMPLEMENTATION_GUIDE.md) | Step-by-step build guide with code and explanations |
| [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md) | All test cases and code review checklist |
| [`docs/CODING_STANDARDS.md`](docs/CODING_STANDARDS.md) | Style guide, naming conventions, anti-patterns |

---

## Requirements

- Python 3.8+
- Zero external dependencies

---

## Architecture in One Diagram

```
User types something
        │
        ▼
  .strip().lower()       ← sanitize
        │
        ├── empty?       → hint + continue
        ├── "quit"?      → farewell + exit
        └── anything else → dict.get(input, fallback) → print response
```

---

## Key Concepts Practiced

| Concept | How It Appears |
|---------|---------------|
| Control flow | `while True`, `if`, `break`, `continue` |
| Hash map / dictionary | `KNOWLEDGE_BASE = {...}` |
| O(1) lookup | `dict.get(key, default)` |
| Input sanitization | `.strip().lower()` |
| Pure functions | `get_response()` — no side effects |
| White box design | Every response is hard-coded and traceable |

---

## Qualification

This project is **mandatory** for all Batch 2026 interns. Completion unlocks subsequent projects. All submissions are reviewed for quality.

---

*DecodeLabs | Greater Lucknow, India | decodelabs.tech@gmail.com*
