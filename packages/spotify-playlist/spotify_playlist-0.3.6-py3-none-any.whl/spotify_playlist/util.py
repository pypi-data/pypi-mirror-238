import logging
import os
import random

import spotipy
import unidecode
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger(__name__)


def save_all_lists(env):
    os.environ.update(env)
    scope = "user-library-modify,playlist-read-private,playlist-modify-private"
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    os.makedirs("playlist", exist_ok=True)
    offset = 0
    count = 0
    while True:
        t = spotify.current_user_playlists(limit=50,offset=offset)["items"]
        for item in t:
            count += 1
            # spotify.playlist_change_details(item['id'], public=False)
            offset_song = 0
            with open(os.path.join("playlist", f"{item['name']}.csv"), 'w', encoding="utf-8") as file:
                while True:
                    tt = spotify.playlist_items(item['id'], offset=offset_song)
                    # print(item, len(tt["items"]))
                    for itemt in tt["items"]:
                        # logger.info(itemt['track']['name'] + " -- " + itemt['track']['album']['name'])
                        file.write('"{}","{}" \n'.format(itemt['track']['album']['name'], itemt['track']['name']))
                    if len(tt["items"]) < 100:
                        break
                    offset_song = offset_song + 100
            logger.info(f"{item['name']} updated")
        if len(t) < 50:
            break
        offset = offset + 50
    logger.info(f"{count} playlists updated")


def save_specific_list(env, names):
    os.environ.update(env)
    scope = "user-library-modify,playlist-read-private,playlist-modify-private"
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    os.makedirs("playlist", exist_ok=True)
    offset = 0
    lower_names = [unidecode.unidecode(name).lower() for name in names]
    while True:
        t = spotify.current_user_playlists(limit=50,offset=offset)["items"]
        for item in t:
            uniname = unidecode.unidecode(item['name']).lower()
            update = False
            for n in lower_names:
                if uniname.startswith(n):
                    update = True
            if update:
                offset_song = 0
                with open(os.path.join("playlist", f"{item['name']}.csv"), 'w', encoding="utf-8") as file:
                    while True:
                        tt = spotify.playlist_items(item['id'], offset=offset_song)
                        # print(item, len(tt["items"]))
                        for itemt in tt["items"]:
                            # logger.info(itemt['track']['name'] + " -- " + itemt['track']['album']['name'])
                            file.write('"{}","{}" \n'.format(itemt['track']['album']['name'], itemt['track']['name']))
                        if len(tt["items"]) < 100:
                            break
                        offset_song = offset_song + 100
                logger.info(f"{item['name']} updated")
        if len(t) < 50:
            break
        offset = offset + 50


def random_list(env):
    os.environ.update(env)
    scope = "user-library-modify,playlist-read-private,playlist-modify-private"
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    playlist = []
    offset = 0
    while True:
        t = spotify.current_user_playlists(limit=50,offset=offset)["items"]
        for item in t:
            playlist.append(item['name'])
        if len(t) < 50:
            break
        offset = offset + 50
    # print(playlist)
    os.system('cls')
    print('\n', random.choice(playlist), '\n')
    while True:
        input("")
        os.system('cls')
        print('\n', random.choice(playlist), '\n')
