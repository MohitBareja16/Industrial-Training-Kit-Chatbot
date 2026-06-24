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

# Terminal Colors for Aesthetics (No External Libraries)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

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
    # Print an aesthetically pleasing banner using ANSI colors
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  {BOT_NAME} — Rule-Based AI Chatbot{Colors.RESET}")
    print(f"{Colors.BLUE}  Type 'help' | Type 'quit' to exit{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 50}{Colors.RESET}\n")

    while True:
        # Green prompt for the user
        raw_input = input(f"{Colors.GREEN}{Colors.BOLD}You:{Colors.RESET} ")
        clean_input = raw_input.strip().lower()

        if not clean_input:
            print(f"{Colors.YELLOW}Bot: (Please type a message.){Colors.RESET}\n")
            continue

        if clean_input in EXIT_COMMANDS:
            print(f"{Colors.HEADER}{Colors.BOLD}Bot: Goodbye! Session ended.{Colors.RESET}\n")
            break

        response = get_response(clean_input)
        # Blue/Purple prompt for the bot
        print(f"{Colors.BLUE}{Colors.BOLD}Bot:{Colors.RESET} {response}\n")

# ── SECTION 5: ENTRYPOINT ─────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        run_chatbot()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}{Colors.BOLD}Bot: Session interrupted. Goodbye!{Colors.RESET}")
