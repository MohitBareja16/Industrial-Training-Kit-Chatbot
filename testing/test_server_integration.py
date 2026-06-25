import os
import sys
import unittest
import threading
import http.client
import json
import time
from http.server import HTTPServer

# Resolve path to include backend directory
TESTING_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(TESTING_DIR, '..'))
sys.path.append(os.path.join(BASE_DIR, 'backend'))

from server import ChatHandler

class TestServerIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start server in background thread on test port 8086
        cls.server_address = ('127.0.0.1', 8086)
        cls.httpd = HTTPServer(cls.server_address, ChatHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        # Allow time for server thread to start
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join()

    def test_get_root(self):
        # Verify GET / serves index.html content correctly
        conn = http.client.HTTPConnection(*self.server_address)
        conn.request('GET', '/')
        res = conn.getresponse()
        self.assertEqual(res.status, 200)
        self.assertEqual(res.getheader('Content-Type'), 'text/html')
        
        # Verify CORS header is present
        self.assertEqual(res.getheader('Access-Control-Allow-Origin'), '*')
        
        body = res.read().decode('utf-8')
        self.assertIn("Decodes Logic Engine", body)
        conn.close()

    def test_options_preflight(self):
        # Verify CORS preflight OPTIONS request returns 204 No Content and CORS headers
        conn = http.client.HTTPConnection(*self.server_address)
        conn.request('OPTIONS', '/chat')
        res = conn.getresponse()
        
        self.assertEqual(res.status, 204)
        self.assertEqual(res.getheader('Access-Control-Allow-Origin'), '*')
        self.assertIn('POST', res.getheader('Access-Control-Allow-Methods'))
        self.assertIn('Content-Type', res.getheader('Access-Control-Allow-Headers'))
        conn.close()

    def test_post_chat_valid(self):
        # Verify POST /chat responds with JSON and correct bot message
        conn = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'message': 'what is ai'})
        conn.request('POST', '/chat', data, headers)
        res = conn.getresponse()
        
        self.assertEqual(res.status, 200)
        self.assertEqual(res.getheader('Content-Type'), 'application/json')
        self.assertEqual(res.getheader('Access-Control-Allow-Origin'), '*')
        
        body = json.loads(res.read().decode('utf-8'))
        self.assertIn('response', body)
        self.assertIn('simulation of human intelligence', body['response'].lower())
        conn.close()

    def test_post_chat_invalid_json(self):
        # Verify invalid JSON returns 400 bad request
        conn = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-Type': 'application/json'}
        data = "{invalid-json}"
        conn.request('POST', '/chat', data, headers)
        res = conn.getresponse()
        
        self.assertEqual(res.status, 400)
        conn.close()

    def test_post_verify_key_invalid(self):
        # Verify invalid API key returns 400 and status failed
        conn = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'api_key': 'invalid_key_123'})
        conn.request('POST', '/verify-key', data, headers)
        res = conn.getresponse()
        
        self.assertEqual(res.status, 400)
        body = json.loads(res.read().decode('utf-8'))
        self.assertEqual(body.get('status'), 'failed')
        conn.close()

    def test_post_chat_am_i_connected_offline(self):
        # Verify "am i connected to llm?" diagnostic returns offline notice when no key is sent
        conn = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'message': 'am i connected to llm?', 'api_key': ''})
        conn.request('POST', '/chat', data, headers)
        res = conn.getresponse()
        
        self.assertEqual(res.status, 200)
        body = json.loads(res.read().decode('utf-8'))
        self.assertIn('please enter a valid gemini api key', body.get('response').lower())
        conn.close()

    def test_heuristic_match(self):
        # Verify Heuristic Mode matches key subsets
        conn = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({
            'message': 'could you explain what coding is?', 
            'mode': 'Heuristic Mode'
        })
        conn.request('POST', '/chat', data, headers)
        res = conn.getresponse()
        
        self.assertEqual(res.status, 200)
        body = json.loads(res.read().decode('utf-8'))
        self.assertIn('art of telling a computer', body.get('response').lower())
        conn.close()

if __name__ == '__main__':
    unittest.main()
