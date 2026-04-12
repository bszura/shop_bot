from flask import Flask
from threading import Thread
import logging

app = Flask('')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord Shop Bot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #2b2d31;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
            }
            .status {
                background: #5865f2;
                padding: 20px 40px;
                border-radius: 10px;
                display: inline-block;
            }
            h1 { margin: 0; }
            p { margin: 10px 0 0 0; opacity: 0.8; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status">
                <h1>✅ Bot is Online</h1>
                <p>Discord Shop Bot is running</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
