import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import sys, codecs, json


ROOT_URL = "https://rock.com.ar"


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


class PyLyricsRockAr:
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
                album_url = f"{ROOT_URL + tag_album['href']}"
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
        url = ROOT_URL + track.link()
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
        url = ROOT_URL + "/artistas/177"
        return Artist(name, url)


def main():
    artist = PyLyricsRockAr.get_artist("Charly Garcia")
    # print(artist)
    albums = PyLyricsRockAr.get_albums(artist)
    # print(albums)
    tracks = PyLyricsRockAr.get_tracks(albums[-1])
    # print(tracks)
    lyric = PyLyricsRockAr.get_lyrics(tracks[3])
    print(lyric)


if __name__ == "__main__":
    main()
