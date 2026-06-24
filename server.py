import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from chatbot import get_response, BOT_NAME

class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                with open('index.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                user_input = data.get('message', '')
                clean_input = user_input.strip().lower()
                
                # Retrieve the response using the existing logic engine
                if not clean_input:
                    bot_reply = "Please type a message."
                elif clean_input in ["quit", "exit"]:
                    bot_reply = "Session ended. Please close the tab or refresh to restart."
                else:
                    bot_reply = get_response(clean_input)
                
                response_data = {'response': bot_reply}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Not found")

def run(server_class=HTTPServer, handler_class=ChatHandler, port=8000):
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
