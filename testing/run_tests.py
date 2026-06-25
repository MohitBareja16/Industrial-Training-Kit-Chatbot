import unittest
import sys
import os

# Resolve paths
TESTING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TESTING_DIR)

def run():
    print("=" * 60)
    print("      DECODELABS CHATBOT QUALITY VERIFICATION SYSTEM")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=TESTING_DIR, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("                     TEST REPORT SUMMARY")
    print("=" * 60)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Passed:          {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:        {len(result.failures)}")
    print(f"Errors:          {len(result.errors)}")
    print("=" * 60)
    
    if not result.wasSuccessful():
        print("Result: FAIL ❌ - Please fix the errors/failures above.")
        sys.exit(1)
    else:
        print("Result: PASS  - All quality gates successfully passed!")
        sys.exit(0)

if __name__ == "__main__":
    run()
