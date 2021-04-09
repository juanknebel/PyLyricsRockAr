from py_lyrics_rock_ar import PyLyricsRockAr
import pandas as pd
import tqdm
import time


def scrap_as_dict():
    album_by_artist = dict()
    # {
    #   artista1: {
    #       almbum1: {cancion1: letra1, cancion2: letra2},
    #       almbum2: {cancion3: letra3, cancion4: letra4}},
    #   artista2: {
    #       almbum3: {cancion5: letra5, cancion6: letra6},
    #       almbum4: {cancion7: letra7, cancion8: letra8}}
    # }
    for an_artist in PyLyricsRockAr.available_artist():
        artist = PyLyricsRockAr.get_artist(an_artist)
        albums = PyLyricsRockAr.get_albums(artist)

        tracks_by_album = dict()
        # {
        #   almbum1: {cancion1: letra1, cancion2: letra2},
        #   almbum2: {cancion3: letra3, cancion4: letra4}
        # }
        for an_album in albums:
            tracks = PyLyricsRockAr.get_tracks(an_album)

            lyrics_by_track = dict()
            # {cancion1: letra1, cancion2: letra2}
            for a_track in tracks:
                lyrics_by_track[a_track.name()] = PyLyricsRockAr.get_lyrics(
                    a_track
                )

            tracks_by_album[an_album.name()] = lyrics_by_track

        album_by_artist[artist.name()] = tracks_by_album
        break

    print(album_by_artist)


def scrap_as_dataframes():
    datasets = []
    # for an_artist in ["La Maquina de Hacer Pajaros"]:
    for an_artist in tqdm.tqdm(PyLyricsRockAr.available_artist()):
        artist = PyLyricsRockAr.get_artist(an_artist)
        time.sleep(1)
        albums = PyLyricsRockAr.get_albums(artist)
        time.sleep(1)
        for an_album in albums:
            tracks = PyLyricsRockAr.get_tracks(an_album)

            lyrics = []
            for a_track in tracks:
                lyrics += [PyLyricsRockAr.get_lyrics(a_track)]

            lyrics_df = pd.DataFrame(
                zip(tracks, lyrics), columns=["track_name", "lyric"]
            )
            lyrics_df["release_year"] = an_album.year()
            lyrics_df["album"] = an_album.name()
            lyrics_df["artist"] = artist.name()

            datasets += [lyrics_df]
            time.sleep(1)
        time.sleep(10) # wait 10 seconds

    if datasets == []:
        raise ImportWarning("No lyric to add.")

    df = pd.concat(datasets)
    df.to_csv("lyrics.csv", index=False, sep=";")


if __name__ == "__main__":
    # PyLyricsRockAr.get_all_the_artists_links()
    # print(PyLyricsRockAr.available_artist())
    scrap_as_dataframes()