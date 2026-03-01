import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- 1. SPOTIFY & AI SETUP ---
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-top-read user-read-recently-played"
))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat = client.chats.create(model="gemini-2.5-flash-lite")

# --- 2. THE ROUTES ---
@app.route('/')
def index():
    # Fetch data to show on the dashboard immediately
    top = sp.current_user_top_tracks(limit=5, time_range='short_term')['items']
    recent = sp.current_user_recently_played(limit=5)['items']
    return render_template('index.html', top=top, recent=recent)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    user_msg = request.json.get('message')
    response = chat.send_message(user_msg)
    return jsonify({"reply": response.text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)