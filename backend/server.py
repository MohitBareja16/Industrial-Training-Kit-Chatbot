import json
import os
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from chatbot import get_response, BOT_NAME, KNOWLEDGE_BASE, FALLBACK_RESPONSE

# Resolve paths relative to backend directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(BACKEND_DIR, '..'))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

def call_gemini(api_key: str, prompt: str) -> str:
    """Send prompt to Gemini API using built-in urllib."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text = res_data['candidates'][0]['content']['parts'][0]['text']
            return text.strip()
    except Exception as e:
        return f"Gemini Pipeline Error: {e}"

def verify_gemini_key(api_key: str) -> bool:
    """Verify Gemini API key validity by querying a simple response."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": "respond only with ok"}]
        }]
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text = res_data['candidates'][0]['content']['parts'][0]['text']
            return len(text) > 0
    except Exception:
        return False

class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Remove query parameters or fragments
        path = self.path.split('?')[0].split('#')[0]
        
        if path == '/':
            filename = 'index.html'
        else:
            filename = path.lstrip('/')
            
        # Decode URL-encoded paths
        filename = urllib.parse.unquote(filename)
        
        # Resolve target filepath inside frontend folder
        filepath = os.path.abspath(os.path.join(FRONTEND_DIR, filename))
        
        # Path traversal guard: verify file is inside FRONTEND_DIR
        if not filepath.startswith(FRONTEND_DIR):
            self.send_error(403, "Forbidden: Path traversal blocked")
            return
            
        if os.path.exists(filepath) and os.path.isfile(filepath):
            # Map extensions to MIME types
            ext = os.path.splitext(filepath)[1].lower()
            mime_types = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
                '.ico': 'image/x-icon',
                '.json': 'application/json'
            }
            content_type = mime_types.get(ext, 'application/octet-stream')
            
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Content-Length', str(len(content)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Internal server error: {e}")
        else:
            self.send_error(404, "File not found")

    def do_OPTIONS(self):
        # Handle CORS preflight request
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                user_input = data.get('message', '')
                api_key = data.get('api_key', '').strip()
                mode = data.get('mode', 'Deterministic Mode').strip()
                
                clean_input = user_input.strip().lower()
                
                # am i connected to llm check (applicable globally)
                if clean_input.rstrip('?.!') == "am i connected to llm":
                    if api_key:
                        is_valid = verify_gemini_key(api_key)
                        if is_valid:
                            bot_reply = "Yes, you are connected to the Gemini LLM pipeline. Status: Active (Gemini 1.5 Flash)."
                        else:
                            bot_reply = "No, you are not connected. The provided Gemini API key is invalid or inactive."
                    else:
                        bot_reply = "No, you are not connected to the LLM pipeline. Please enter a valid Gemini API key in the sidebar settings."
                elif not clean_input:
                    bot_reply = "Please type a message."
                elif clean_input in ["quit", "exit"]:
                    bot_reply = "Session ended. Please close the tab or refresh to restart."
                else:
                    if mode == "Deterministic Mode":
                        # Pure direct matching
                        bot_reply = get_response(clean_input)
                    elif mode == "Heuristic Mode":
                        # Exact check first
                        res = get_response(clean_input)
                        if res != FALLBACK_RESPONSE:
                            bot_reply = res
                        else:
                            # Heuristic matching: find best word overlap
                            input_words = set(clean_input.rstrip('?.!').split())
                            match = None
                            best_overlap = 0
                            for key, value in KNOWLEDGE_BASE.items():
                                if key in ["quit", "exit"]:
                                    continue
                                key_words = set(key.split())
                                overlap = key_words.intersection(input_words)
                                # Must match at least 60% of the key words, and at least 1 word
                                if len(overlap) > 0 and len(overlap) >= len(key_words) * 0.6:
                                    if len(overlap) > best_overlap:
                                        best_overlap = len(overlap)
                                        match = value
                            bot_reply = match if match else FALLBACK_RESPONSE
                    elif mode == "Hybrid Pipeline":
                        # Tier 1: Deterministic check
                        res = get_response(clean_input)
                        if res != FALLBACK_RESPONSE:
                            bot_reply = res
                        elif api_key:
                            # Tier 2: Generative fallback using Gemini LLM
                            bot_reply = call_gemini(api_key, user_input)
                        else:
                            bot_reply = res
                    else:
                        bot_reply = get_response(clean_input)
                
                response_data = {'response': bot_reply}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                
        elif self.path == '/verify-key':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                api_key = data.get('api_key', '').strip()
                is_valid = verify_gemini_key(api_key)
                
                response_data = {'status': 'connected' if is_valid else 'failed'}
                self.send_response(200 if is_valid else 400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Not found")

def run(server_class=HTTPServer, handler_class=ChatHandler, port=8085):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"========================================")
    print(f" {BOT_NAME} Web Interface Running!")
    print(f" Open http://localhost:{port} in your browser")
    print(f"========================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    run()
