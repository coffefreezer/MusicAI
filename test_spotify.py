import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# This is the "Handshake" configuration
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    # We are adding 'recently-played' to see your Current Vibe
    scope = "user-top-read user-read-recently-played"
))

try:
    user = sp.current_user()
    print(f"\n✅ SUCCESS! Connected to: {user['display_name']}")
    
    # Let's see your top 5 tracks just for fun
    print("\n🎸 Your Top 5 Recent Tracks:")
    top_tracks = sp.current_user_top_tracks(limit=5, time_range='short_term')
    for i, track in enumerate(top_tracks['items']):
        print(f"{i+1}. {track['name']} by {track['artists'][0]['name']}")

except Exception as e:
    print(f"❌ Connection failed: {e}")