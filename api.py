#!/usr/bin/env python3 
from flask import Flask, jsonify, request 
from flask_cors import CORS 
import mysql.connector 
from dotenv import load_dotenv
import os

load_dotenv()
 
app = Flask(__name__) 
CORS(app) 
 
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
 
@app.route('/api/messages', methods=['GET']) 
def get_messages(): 
    """Hae viestit tietokannasta.""" 
    limit = request.args.get('limit', 50, type=int) 
    conn = mysql.connector.connect(**DB_CONFIG) 
    cursor = conn.cursor(dictionary=True) 
    cursor.execute(''' 
        SELECT id, nickname, message, client_id, created_at 
        FROM messages ORDER BY created_at DESC LIMIT %s 
    ''', (limit,)) 
    messages = cursor.fetchall() 
    for msg in messages: 
        msg['created_at'] = msg['created_at'].isoformat() 
    cursor.close() 
    conn.close() 
    return jsonify(messages[::-1]) 
 
if __name__ == '__main__': 
    app.run(host='127.0.0.1', port=5000) 