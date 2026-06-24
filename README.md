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
