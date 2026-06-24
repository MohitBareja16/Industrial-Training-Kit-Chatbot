"""
chatbot.py
──────────
Project 1: Rule-Based AI Chatbot
DecodeLabs Industrial Training Kit | Batch 2026
Author: DecodeLabs Intern | Date: 2026-06-24
"""

# ── SECTION 1: CONFIGURATION ──────────────────────────────────────────────────

BOT_NAME = "DecodesBot"

EXIT_COMMANDS = frozenset({"quit", "exit"})

FALLBACK_RESPONSE = (
    "I don't understand that yet. "
    "Type 'help' to see what I can do."
)
