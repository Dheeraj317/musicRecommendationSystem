import pickle
import streamlit as st
import pandas as pd 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# Spotify API credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_song_url = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_song_url.append(get_song_urls(music.iloc[i[0]].song))
    return recommended_music_names, recommended_music_posters,recommended_song_url

st.header('Music Recommender System')
music_dict = pickle.load(open('music_dict.pkl', 'rb'))
music = pd.DataFrame(music_dict)
similarity_dict = pickle.load(open('similarity_music.pkl', 'rb'))
similarity = pd.DataFrame(similarity_dict)

music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)
def get_song_urls(song_name):
    song_urls = {}
    search_query = f"track:{song_name}"
    results = sp.search(q=search_query, type="track", limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        song_urls = track['external_urls']['spotify']
    else:
        song_urls = "Not Found"
    time.sleep(0.1)  # To respect the rate limit
    return song_urls

      



if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters, recommended_song_url = recommend(selected_song)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
        st.markdown(f"[Listen on Spotify]({recommended_song_url[0]})")

    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])
        st.markdown(f"[Listen on Spotify]({recommended_song_url[1]})")
    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
        st.markdown(f"[Listen on Spotify]({recommended_song_url[2]})")
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
        st.markdown(f"[Listen on Spotify]({recommended_song_url[3]})")
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])
        st.markdown(f"[Listen on Spotify]({recommended_song_url[4]})")