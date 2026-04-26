import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.core.agent import agent

class TestAgent(unittest.TestCase):
    def test_agent_response(self):
        try:
            response = agent.run("Hello")
            self.assertIsNotNone(response)
            self.assertIsNotNone(response.content)
            print(f"\nAgent Response: {response.content}")
        except Exception as e:
            self.fail(f"Agent raised exception: {e}")

if __name__ == "__main__":
    unittest.main()
