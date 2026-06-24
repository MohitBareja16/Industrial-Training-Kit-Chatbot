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
    # Greetings & Exits
    "hello":         "Hello! How can I help you today?",
    "hi":            "Hey there! What can I do for you?",
    "hey":           "Hi! Ask me anything.",
    "good morning":  "Good morning! I hope you're having a great day.",
    "good evening":  "Good evening! How can I assist you tonight?",
    "good night":    "Good night! I'll be here if you need me.",
    "what's up":     "Not much, just processing some data! How about you?",
    "sup":           "Just hanging out in the RAM. What's on your mind?",
    "thanks":        "You're welcome!",
    "thank you":     "Happy to help!",
    "bye":           "Goodbye! (Type 'quit' to actually exit.)",
    "goodbye":       "See you! (Type 'quit' to end the session.)",

    # Bot Identity & Status
    "how are you":   "All systems running perfectly — I'm deterministic, after all!",
    "who are you":   f"I am {BOT_NAME}, a rule-based AI at DecodeLabs.",
    "what is your name": f"My name is {BOT_NAME}.",
    "how old are you": "Age is just a number. For me, it's the number of seconds since my script started!",
    "where are you from": "I live in your computer's memory, running on DecodeLabs architecture.",
    "who created you": "I was created by an intern at DecodeLabs.",
    "are you a human": "No, I am purely lines of Python code.",
    "are you a robot": "I am a virtual robot, also known as a chatbot.",
    "do you have feelings": "I don't have feelings, but my code executes very happily!",
    "are you alive": "I am alive in the sense that my event loop is running.",

    # Casual Chat & Fun
    "tell me a joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
    "joke":          "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "what is your favorite color": "I'm quite fond of terminal green and Python blue.",
    "what do you do": "I sit in a while loop waiting for you to ask me things.",
    "do you like music": "I love algorithmic music. Have you heard of Kraftwerk?",
    "what is the meaning of life": "42. But also, compiling without errors.",

    # Educational / AI Topics
    "what is ai":    "AI is the simulation of human intelligence by machines.",
    "what is machine learning": "ML is a subset of AI where systems learn from data.",
    "what is a chatbot": "A chatbot is software that simulates human conversation.",
    "what is a rule based system": "A rule-based system uses predefined logic — deterministic and traceable.",
    "what is python": "Python is an awesome, readable programming language. It's what I'm written in!",
    "what is coding": "Coding is the art of telling a computer exactly what to do.",

    # Assistance
    "help":          "I can answer questions about AI, chat casually, or tell jokes. Type 'quit' to exit.",
    "what can you do": "I can talk about AI, tell programming jokes, and chat about my existence.",
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
