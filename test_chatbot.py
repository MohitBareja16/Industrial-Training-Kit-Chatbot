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
