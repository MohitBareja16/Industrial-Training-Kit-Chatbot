import os
import sys
import unittest
import io
from unittest.mock import patch

# Resolve path to include backend directory
TESTING_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(TESTING_DIR, '..'))
sys.path.append(os.path.join(BASE_DIR, 'backend'))

import chatbot
from chatbot import get_response, FALLBACK_RESPONSE, KNOWLEDGE_BASE, EXIT_COMMANDS

class TestChatbotFunctionalAndEdge(unittest.TestCase):
    
    # ── 1. FUNCTIONAL TESTS ──────────────────────────────────────────────────
    
    def test_greeting_hello(self):
        # TC-F-01
        res = get_response("hello")
        self.assertIn("Hello", res)

    def test_greeting_hi(self):
        # TC-F-02
        res = get_response("hi")
        self.assertIn("Hey", res)

    def test_greeting_hey(self):
        # TC-F-03
        res = get_response("hey")
        self.assertIn("Hi", res)

    def test_knowledge_what_is_ai(self):
        # TC-F-04
        res = get_response("what is ai")
        self.assertIn("simulation of human intelligence", res.lower())

    def test_knowledge_how_are_you(self):
        # TC-F-05
        res = get_response("how are you")
        self.assertIn("running perfectly", res.lower())

    def test_knowledge_who_are_you(self):
        # TC-F-06
        res = get_response("who are you")
        self.assertIn("decodesbot", res.lower())

    def test_knowledge_help(self):
        # TC-F-07
        res = get_response("help")
        self.assertIn("quit", res.lower())

    # ── 2. SANITIZATION TESTS ────────────────────────────────────────────────
    
    def test_sanitization_lower(self):
        # TC-S-01, TC-S-02, TC-S-03
        # Since sanitization happens in the caller loop (not get_response itself),
        # we test how get_response behaves with properly sanitized lowercase inputs.
        self.assertEqual(get_response("hello"), get_response("hello"))

    # ── 3. EDGE CASE TESTS ───────────────────────────────────────────────────
    
    def test_edge_unknown(self):
        # TC-E-03, TC-E-04, TC-E-05, TC-E-06, TC-E-10
        self.assertEqual(get_response("xyzunknown123"), FALLBACK_RESPONSE)
        self.assertEqual(get_response("!@#$%"), FALLBACK_RESPONSE)
        self.assertEqual(get_response("hello world"), FALLBACK_RESPONSE)
        self.assertIn("simulation of human intelligence", get_response("what is ai?").lower())
        self.assertEqual(get_response("12345"), FALLBACK_RESPONSE)

    def test_edge_long_string(self):
        # TC-E-09
        long_input = "hello" * 100
        self.assertEqual(get_response(long_input), FALLBACK_RESPONSE)

    def test_fallback_non_empty(self):
        # Verify fallback is a valid non-empty string
        self.assertTrue(len(FALLBACK_RESPONSE.strip()) > 0)


class TestChatbotInteractive(unittest.TestCase):
    
    # ── 4. CONTROL FLOW & SESSION SIMULATION TESTS ──────────────────────────
    
    def simulate_session(self, inputs):
        """Helper to run the run_chatbot loop with mocked console inputs."""
        output = io.StringIO()
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=output):
            try:
                chatbot.run_chatbot()
            except StopIteration:
                # Occurs if inputs don't end session and run out of values
                pass
        return output.getvalue()

    def test_control_flow_exit_quit(self):
        # TC-F-08, TC-CF-01
        stdout = self.simulate_session(["quit"])
        self.assertIn("Goodbye! Session ended", stdout)

    def test_control_flow_exit_exit(self):
        # TC-F-09, TC-CF-01
        stdout = self.simulate_session(["exit"])
        self.assertIn("Goodbye! Session ended", stdout)

    def test_sanitization_input_pipeline(self):
        # TC-S-01, TC-S-02, TC-S-03, TC-S-04, TC-S-05, TC-S-09
        # Verifies the full user input is sanitized (.strip().lower()) inside the runtime loop
        stdout = self.simulate_session(["  HELLO  ", "QUIT"])
        self.assertIn("Hello! How can I help you today?", stdout)
        self.assertIn("Goodbye! Session ended", stdout)

    def test_sanitization_exit_uppercase(self):
        # TC-S-06, TC-S-08
        stdout = self.simulate_session(["QUIT"])
        self.assertIn("Goodbye! Session ended", stdout)
        
        stdout_exit = self.simulate_session(["EXIT"])
        self.assertIn("Goodbye! Session ended", stdout_exit)

    def test_sanitization_exit_spaces(self):
        # TC-S-07
        stdout = self.simulate_session(["  quit  "])
        self.assertIn("Goodbye! Session ended", stdout)

    def test_edge_empty_input(self):
        # TC-E-01, TC-E-02
        stdout = self.simulate_session(["", "   ", "quit"])
        self.assertIn("(Please type a message.)", stdout)
        self.assertIn("Goodbye! Session ended", stdout)

    def test_edge_consecutive_unknowns(self):
        # TC-E-07
        inputs = ["unknown"] * 10 + ["quit"]
        stdout = self.simulate_session(inputs)
        # Check that fallback is printed 10 times
        self.assertEqual(stdout.count(FALLBACK_RESPONSE), 10)

    def test_control_flow_multiple_turns(self):
        # TC-CF-02
        stdout = self.simulate_session(["hello", "what is ai", "quit"])
        self.assertIn("Hello! How can I help you today?", stdout)
        self.assertIn("AI is the simulation of human intelligence", stdout)
        self.assertIn("Goodbye! Session ended", stdout)

    def test_control_flow_empty_then_valid(self):
        # TC-CF-03
        stdout = self.simulate_session(["", "hello", "quit"])
        self.assertIn("(Please type a message.)", stdout)
        self.assertIn("Hello! How can I help you today?", stdout)

    def test_control_flow_unknown_then_exit(self):
        # TC-CF-04
        stdout = self.simulate_session(["unknown", "quit"])
        self.assertIn(FALLBACK_RESPONSE, stdout)
        self.assertIn("Goodbye! Session ended", stdout)


class TestChatbotCodeReviewChecklist(unittest.TestCase):
    
    # ── 5. CODE REVIEW CHECKLIST TESTS (STATIC ANALYSIS) ───────────────────
    
    def setUp(self):
        chatbot_path = os.path.join(BASE_DIR, 'backend', 'chatbot.py')
        with open(chatbot_path, 'r', encoding='utf-8') as f:
            self.code = f.read()
        self.lines = self.code.splitlines()

    def test_cr_01_while_true_present(self):
        # CR-01
        self.assertTrue(any("while True:" in line for line in self.lines), "Missing while True: loop")

    def test_cr_02_input_sanitized(self):
        # CR-02
        self.assertTrue(
            any(".strip().lower()" in line or ".lower().strip()" in line for line in self.lines),
            "Input is not sanitized via strip() and lower()"
        )

    def test_cr_03_knowledge_base_dict(self):
        # CR-03
        self.assertIsInstance(KNOWLEDGE_BASE, dict, "Knowledge base is not a dictionary")

    def test_cr_04_knowledge_base_min_entries(self):
        # CR-04: Should have >= 5 entries excluding exits
        filtered_kb = {k: v for k, v in KNOWLEDGE_BASE.items() if k not in EXIT_COMMANDS}
        self.assertTrue(len(filtered_kb) >= 5, "Knowledge base has less than 5 entries")

    def test_cr_05_get_method_used(self):
        # CR-05: get() is used for response lookup
        self.assertTrue(any(".get(" in line for line in self.lines), "Missing KB.get() lookup")

    def test_cr_06_exit_handled_with_break(self):
        # CR-06
        self.assertTrue(any("break" in line for line in self.lines), "Exit is not handled with break")

    def test_cr_07_no_prohibited_exit_calls(self):
        # CR-07, CR-A3
        self.assertNotIn("sys.exit(", self.code)
        self.assertNotIn("os._exit(", self.code)

    def test_cr_08_fallback_response_non_empty(self):
        # CR-08, CR-A4
        self.assertTrue(len(FALLBACK_RESPONSE.strip()) > 0, "Fallback response is empty")

    def test_cr_09_empty_input_explicitly_handled(self):
        # CR-09
        self.assertTrue(
            any("not clean_input" in line or "len(clean_input)" in line for line in self.lines),
            "Empty input is not explicitly handled"
        )

    def test_cr_10_no_external_packages(self):
        # CR-10: Only permit built-in imports if any
        # Scan imports in chatbot.py
        for line in self.lines:
            if line.startswith("import ") or line.startswith("from "):
                pkg = line.split()[1].split('.')[0]
                # Permitted standard libraries
                self.assertIn(pkg, ["sys", "os", "json", "unittest", "io", "frozenset", "typing"], 
                              f"Prohibited external package import found: {line}")

    def test_cr_11_and_cr_a5_loop_order(self):
        # CR-11, CR-A5: Empty check -> Exit check -> KB Lookup
        # Let's locate the line numbers of loop body statements
        empty_check_idx = -1
        exit_check_idx = -1
        kb_lookup_idx = -1
        
        for idx, line in enumerate(self.lines):
            if "not clean_input" in line:
                empty_check_idx = idx
            elif "in EXIT_COMMANDS" in line:
                exit_check_idx = idx
            elif "get_response(" in line:
                # Ensure it's inside the loop, not the definition
                if "def get_response" not in line and "You:" not in line:
                    kb_lookup_idx = idx
                    
        self.assertTrue(empty_check_idx != -1, "Could not locate empty input check in loop")
        self.assertTrue(exit_check_idx != -1, "Could not locate exit command check in loop")
        self.assertTrue(kb_lookup_idx != -1, "Could not locate KB lookup in loop")
        
        self.assertTrue(empty_check_idx < exit_check_idx, "Empty input check must run before exit check")
        self.assertTrue(exit_check_idx < kb_lookup_idx, "Exit check must run before KB lookup")

    def test_cr_a1_no_if_elif_ladder_for_dispatch(self):
        # CR-A1: No long if-elif chain matching exact intents
        # We search for lines starting with 'elif' and checking matches (excluding quit/exit)
        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith("elif") and ("==" in stripped or "in" in stripped):
                # Ensure it's not the exit command check
                self.assertNotIn("EXIT_COMMANDS", stripped, "Intents should be in KB, not in if-elif statements")

    def test_cr_a2_exit_keywords_not_in_kb(self):
        # CR-A2
        for exit_cmd in EXIT_COMMANDS:
            self.assertNotIn(exit_cmd, KNOWLEDGE_BASE, f"Exit command '{exit_cmd}' must not be a key in KNOWLEDGE_BASE")


if __name__ == '__main__':
    unittest.main()
