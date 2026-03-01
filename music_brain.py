import os
import io
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google import genai  # <--- The new import
from google.genai import types # <--- For configurations
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

# --- 1. SPOTIFY SETUP ---
scope = "user-top-read user-read-recently-played"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope=scope
))

def get_music_context():
    try:
        top = sp.current_user_top_tracks(limit=5, time_range='long_term')
        recent = sp.current_user_recently_played(limit=10)
        
        general = [f"{t['name']} by {t['artists'][0]['name']}" for t in top['items']]
        current = [f"{item['track']['name']} by {item['track']['artists'][0]['name']}" for item in recent['items']]
        return general, current
    except Exception as e:
        print(f"Spotify Error: {e}")
        return [], []

# --- 2. NEW 2026 AI SETUP ---
# In the new SDK, we create a client first
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Use gemini-2.0-flash (the 2026 standard) or gemini-1.5-flash
MODEL_ID = "gemini-2.5-flash-lite"

system_prompt = """
You are 'VibeCheck', a music strategist. 
Logic: 
- 'Song now' = use Current Vibe. 
- 'Playlist' = use General Taste.
- Always ask 1 music discovery question at the end.
"""

# --- 3. RUNNING THE APP ---
def run_app():
    general, current = get_music_context()
    
    # In the new SDK, chat is created like this:
    chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    # Initial context handshake
    context_msg = f"SYSTEM DATA: General={general}, Current={current}"
    chat.send_message(context_msg)

    print(f"🎵 VibeCheck 2026 Online (using {MODEL_ID})")
    print("-" * 30)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            break

        response = chat.send_message(user_input)
        print(f"\nAI: {response.text}\n")

if __name__ == "__main__":
    run_app()