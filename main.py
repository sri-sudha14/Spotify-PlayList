import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

year = input("Which year do you want to travel?\nType date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{year}/")
data = response.text

soup = BeautifulSoup(data, "html.parser")
songs =[each.get_text().strip() for each in soup.select("li ul li h3")]
song_names=[]
for song in songs:
    song_names.append(song)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="",
        client_secret="",
        show_dialog=True,
        cache_path="token.txt",
        username="",
    )
)
user_id = sp.current_user()["id"]


song_uris = []
date = year.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{date}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)