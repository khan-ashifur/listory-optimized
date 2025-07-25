#!/usr/bin/env python3
"""
Simple HTTP server for development testing
This is a fallback if Django is not working
"""
import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

PORT = 8000

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Mock response for API endpoints
            response = {
                "id": 1,
                "message": "Django server not running. Please start Django with: python manage.py runserver",
                "status": "mock_response"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_POST()

    def do_GET(self):
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                "message": "Mock API response - Django server not running",
                "hint": "Start Django with: python manage.py runserver"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        print(f"Mock server serving at http://localhost:{PORT}")
        print("This is a fallback server - you should start Django instead")
        print("Run: python manage.py runserver")
        httpd.serve_forever()