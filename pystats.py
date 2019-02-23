import spotipy
from flask import Flask
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

app = Flask(__name__)

@app.route('/index')
def index():
    cid = "10de425754a24e64a4310b06b5ec4500"
    secret = "af680065d39d41ddbaa209a27fb3d14a"
    username = ""
    artists = []

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    scope = 'user-library-read user-top-read'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        topartists_long = sp.current_user_top_artists(limit=50, offset=0, time_range='long_term')
        result = ""
        for artist in topartists_long['items']:
            artists.append(artist['name'])
        result = '<br/>'.join(artists)
        return "Top 50 artists (all time):<br/> %s" % result
            #return artist['name']
            #print(artist['name'])


    else:
        print("Can't get token for", username)



if __name__ == "__main__":
    app.run(debug=True)

#clientID = "10de425754a24e64a4310b06b5ec4500"
#clientSecret = "af680065d39d41ddbaa209a27fb3d14a"
