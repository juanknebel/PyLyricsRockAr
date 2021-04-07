import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import sys, codecs, json


class Track(object):
    def __init__(self, track_name, link, album):
        self._track_name = track_name
        self._album = album
        self._link = link
        self._lyrics = None

    def link(self):
        return self._link

    def __repr__(self):
        return self._track_name

    def lyrics(self):
        if self._lyrics is None:
            self._lyrics = PyLyricsRockAr.get_lyrics(self)
        return self._lyrics

    def name(self):
        return self._track_name


class Artist(object):
    def __init__(self, name, link):
        self._name = name
        self._link = link
        self._albums = None

    def link(self):
        return self._link

    def albums(self):
        if self._albums is None:
            self._albums = PyLyricsRockAr.get_albums(self)
        return self._albums

    def __repr__(self):
        return self._name

    def name(self):
        return self._name


class Album(object):
    def __init__(self, name, year, link, artist):
        self._year = year
        self._name = name
        self._link = link
        self._artist = artist
        self._tracks = None

    def link(self):
        return self._link

    def __repr__(self):
        return self._name

    def artist(self):
        return self._artist

    def tracks(self):
        if self._tracks is None:
            self._tracks = PyLyricsRockAr.get_tracks(self)
        return self._tracks

    def name(self):
        return self._name

    def year(self):
        return self._year


class PyLyricsRockAr:
    ROOT_URL = "https://rock.com.ar"

    _available_artist = {
        "Charly Garcia": 177,
        "Luis Alberto Spinetta": 73,
        "Soda Stereo": 200,
        "Seru Giran": 260,
        "Sui Generis": 262,
        "Miguel Abuelo": 39,
        "Los Abuelos de la Nada": 38,
        "Pacha Santa": 17775,
        "La Maquina de Hacer Pajaros": 361,
    }

    @staticmethod
    def get_albums(artist):
        url = f"{artist.link()}/discos"
        albums_response = BeautifulSoup(
            requests.get(url).text, features="html.parser"
        )

        main_body = albums_response.find("div", "post-content-text")

        discography = (
            main_body.find("div", "comments")
            .find("ul", "comments__list")
            .find_all("li")
        )

        albums = []

        for li_album in discography:
            try:
                tag_album = li_album.find(
                    "h3", "comments__list-item-title"
                ).find("a", href=True)
                album_name = tag_album.text
                album_url = f"{PyLyricsRockAr.ROOT_URL + tag_album['href']}"
                album_year = int(
                    li_album.find(
                        "span", "comments__list-item-date"
                    ).text.split(": ")[1]
                )
                albums += [Album(album_name, album_year, album_url, artist)]
            except:
                pass

        if albums == []:
            raise ValueError("Unknown Artist Name given")
            return None
        return albums

    @staticmethod
    def get_tracks(album):
        tracks_response = BeautifulSoup(
            requests.get(album.link()).text, features="html.parser"
        )

        tracks_body = tracks_response.find("ol", "tracklisting")

        songs = []
        for li_track in tracks_body.find_all("li"):
            link = None
            name = li_track.text.strip()
            if li_track.find("a", href=True) is not None:
                link = li_track.find("a", href=True)["href"]

            songs += [Track(name, link, album)]

        return songs

    @staticmethod
    def get_lyrics(track):
        if track.link() is None:
            return None
        url = PyLyricsRockAr.ROOT_URL + track.link()
        lyrics_response = BeautifulSoup(
            requests.get(url).text, features="html.parser"
        )

        # Get main lyrics holder
        lyrics_body = lyrics_response.find("div", "post-content-text").find(
            "div", {"class": None}
        )

        return lyrics_body.text.strip()

    @staticmethod
    def get_artist(name):
        try:
            url = (
                PyLyricsRockAr.ROOT_URL
                + "/artistas/"
                + str(PyLyricsRockAr._available_artist[name])
            )
            return Artist(name, url)
        except KeyError:
            raise ValueError(f"The artist {name} is not yet mapped.")

    @staticmethod
    def available_artist():
        return list(PyLyricsRockAr._available_artist.keys())


def main():
    artist = PyLyricsRockAr.get_artist("Charly Garcia")
    print(artist)
    albums = PyLyricsRockAr.get_albums(artist)
    print(albums)
    tracks = PyLyricsRockAr.get_tracks(albums[-1])
    print(tracks)
    lyric = PyLyricsRockAr.get_lyrics(tracks[3])
    print(lyric)


if __name__ == "__main__":
    main()
    # print(PyLyricsRockAr.available_artist())
