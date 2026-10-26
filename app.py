from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Quotex Ultra-Pro Max Live Engine Running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def start_server():
    server_thread = threading.Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()
