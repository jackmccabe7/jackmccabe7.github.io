#THIS VERSION WORKS, GOD BLESS
#uses bottle instead of flask to handle user authorisation but works much the same as before

from bottle import route, run, request
import spotipy
from spotipy import oauth2

#PORT_NUMBER = 8888
SPOTIPY_CLIENT_ID = '7730860bf70a42aba37104ee5ae6fc09'
SPOTIPY_CLIENT_SECRET = '208090a49a554342bd669bf0da06fda5'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/'
SCOPE = 'user-library-read user-top-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)

@route('/')
def index():

    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        artists = []
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        topartists_long = sp.current_user_top_artists(limit=50, offset=0, time_range='long_term')
        result = ""
        for artist in topartists_long['items']:
            artists.append(artist['name'])
        result = '<br/>'.join(artists)
        return "Top 50 artists (all time):<br/> %s" % result

    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host='localhost')
