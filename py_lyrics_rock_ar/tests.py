import unittest

try:
    from .__init__ import *  # Python 3
except:
    from __init__ import *

try:
    basestring = basestring
except NameError:
    basestring = (str, bytes)

artist = PyLyricsRockAr.get_artist("Charly Garcia")
albums = PyLyricsRockAr.get_albums(artist)
tracks = PyLyricsRockAr.get_tracks(albums[-1])


class PyLyricsTest(unittest.TestCase):
    def test_albums(self):
        self.assertIsInstance(albums, list)

    def test_tracks(self):
        self.assertIsInstance(albums[0].tracks(), list)

    def test_lyrics(self):
        self.assertIsInstance(PyLyricsRockAr.get_lyrics(tracks[3]), basestring)


if __name__ == "__main__":
    unittest.main()
