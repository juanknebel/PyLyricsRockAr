import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import sys, codecs, json
import logging


logging.basicConfig(filename="error.log", level=logging.INFO)


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

    def album(self):
        return self._album


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


def load_artists(file_name):
    default_artists = dict()
    try:
        with open(file_name, "r") as file_in:
            json_artists = file_in.read()
            default_artists = json.loads(json_artists)
    except FileNotFoundError:
        logging.info(
            f"The file {file_name} not exist, using the default artists list"
        )
        default_artists = {
            "Charly García": 177,
            "Luis Alberto Spinetta": 73,
            "Soda Stereo": 200,
            "Seru Giran": 260,
            "Sui Generis": 262,
            "Miguel Abuelo": 39,
            "Los Abuelos de la Nada": 38,
            "Pacha Santa": 17775,
            "La Máquina de Hacer Pájaros": 361,
        }
    finally:
        return default_artists


class PyLyricsRockAr:
    ROOT_URL = "https://rock.com.ar"
    _artist_file_name = "./available_artists.json"
    _available_artist = load_artists("./available_artists.json")

    @staticmethod
    def get_albums(artist):
        url = f"{PyLyricsRockAr.ROOT_URL + artist.link()}/discos"
        albums_response = BeautifulSoup(
            requests.get(url).text, features="html.parser"
        )
        main_body = albums_response.find("div", "post-content-text")

        albums = []
        try:
            discography = (
                main_body.find("div", "comments")
                .find("ul", "comments__list")
                .find_all("li")
            )

            for li_album in discography:
                tag_album = li_album.find(
                    "h3", "comments__list-item-title"
                ).find("a", href=True)
                album_name = tag_album.text
                album_url = tag_album["href"]
                album_year = li_album.find(
                    "span", "comments__list-item-date"
                ).text.split(": ")[1]
                albums += [Album(album_name, album_year, album_url, artist)]
        except Exception as ex:
            logging.info(
                f"Can't create an album for the artist {artist}. Error: {ex.args[0]}"
            )
        return albums

    @staticmethod
    def get_tracks(album):
        tracks_response = BeautifulSoup(
            requests.get(PyLyricsRockAr.ROOT_URL + album.link()).text,
            features="html.parser",
        )

        songs = []
        try:
            tracks_body = tracks_response.find("ol", "tracklisting")
            for li_track in tracks_body.find_all("li"):
                link = None
                name = li_track.text.strip()
                if li_track.find("a", href=True) is not None:
                    link = li_track.find("a", href=True)["href"]

                songs += [Track(name, link, album)]
        except Exception as ex:
            logging.info(
                f"Can't reach the tracks of {album.artist()} - {album} doesn't have any track. Error: {ex.args[0]}"
            )
        return songs

    @staticmethod
    def get_lyrics(track):
        if track.link() is None:
            return None
        url = PyLyricsRockAr.ROOT_URL + track.link()
        lyrics_response = BeautifulSoup(
            requests.get(url).text, features="html.parser"
        )

        the_lyric = None
        # Get main lyrics holder
        try:
            lyrics_div = lyrics_response.find("div", "post-content-text")
            lyrics_body = lyrics_div.find("div", {"class": None})
            the_lyric = lyrics_body.text.strip()
        except Exception as ex:
            logging.info(
                f"Can reach the lyrics {track.album().artist()} - {track.album()} - {track}. Error: {ex.args[0]}"
            )
        return the_lyric

    @staticmethod
    def get_artist(name):
        try:
            url = PyLyricsRockAr._available_artist[name]
            return Artist(name, url)
        except KeyError:
            raise ValueError(
                f"The artist {name} is not the available artist list."
            )

    @staticmethod
    def available_artist():
        """
        Returns all the available artists that you can scrap the info.
        """
        return list(PyLyricsRockAr._available_artist.keys())

    @staticmethod
    def get_all_the_artists_links():
        """
        This method scrap all the artits names and links and creates a file in your
        current directory named available_artists.json that hold all the links for
        all the artists in the website.
        """
        PyLyricsRockAr._available_artist = dict()
        main_response = BeautifulSoup(
            requests.get(PyLyricsRockAr.ROOT_URL).text, features="html.parser"
        )
        abctop = main_response.find("div", "abctop").find_all("a", href=True)

        for an_entry in abctop:
            search_url = PyLyricsRockAr.ROOT_URL + an_entry["href"]
            search_body = BeautifulSoup(
                requests.get(search_url).text, features="html.parser"
            )
            artists = (
                search_body.find("div", "post-content-text")
                .find("ul", "canciones")
                .find_all("li")
            )

            for an_artist in artists:
                artist_info = an_artist.find("a", href=True)
                PyLyricsRockAr._available_artist[
                    artist_info.text.strip()
                ] = artist_info["href"]

        json_artists = json.dumps(
            PyLyricsRockAr._available_artist, ensure_ascii=False
        )
        with open(PyLyricsRockAr._artist_file_name, "w") as file_out:
            file_out.write(json_artists)


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
    # main()
    # PyLyricsRockAr.get_all_the_artists_links()
    print(PyLyricsRockAr.available_artist())
