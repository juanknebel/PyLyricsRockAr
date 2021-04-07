import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import sys, codecs, json


ROOT_URL = "https://rock.com.ar"


class Track(object):
    def __init__(self, trackName, link, album):
        self.name = trackName
        self.album = album
        self.url = link

    def link(self):
        return self.url

    def __repr__(self):
        return self.name

    def getLyrics(self):
        return PyLyrics.getLyrics(self)


class Artist(object):
    def __init__(self, name, link):
        self.name = name
        self.url = link

    def link(self):
        return self.url

    def getAlbums(self):
        return PyLyrics.getAlbums(self)

    def __repr__(self):
        return self.name


class Album(object):
    def __init__(self, name, year, link, singer):
        self.year = year
        self.name = name
        self.url = link
        self.singer = singer

    def link(self):
        return self.url

    def __repr__(self):
        if sys.version_info[0] == 2:
            return self.name.encode("utf-8", "replace")
        return self.name

    def artist(self):
        return self.singer

    def tracks(self):
        return PyLyrics.getTracks(self)


class PyLyrics:
    @staticmethod
    def getAlbums(singer):
        url = f"{singer.link()}/discos"
        albums_response = BeautifulSoup(
            requests.get(url).text, features="html.parser"
        )

        main_body = albums_response.find("div", "post-content-text")
        artist = main_body.find("h1").text

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
    def getTracks(album):
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
    def getLyrics(track):
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
    def getArtist(name):
        url = ROOT_URL + "/artistas/177"
        return Artist(name, url)


def main():
    artist = PyLyrics.getArtist("Charly Garcia")
    # print(artist)
    albums = PyLyrics.getAlbums(artist)
    # print(albums)
    tracks = PyLyrics.getTracks(albums[-1])
    # print(tracks)
    lyric = PyLyrics.getLyrics(tracks[3])
    print(lyric)


if __name__ == "__main__":
    main()
