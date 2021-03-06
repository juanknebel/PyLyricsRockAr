from setuptools import setup

try:
    import pypandoc

    description = pypandoc.convert("README.md", "rst")

except:
    description = ""
setup(
    name="PyLyricsRockAr",
    version="0.0.1",
    description="Pythonic Implementation of https://rock.com.ar/.",
    long_description=description,
    author="Juan Knebel",
    author_email="juanknebel@gmail.com",
    license="MIT",
    packages=["py_lyrics_rock_ar"],
    url="https://github.com/juanknebel/PyLyricsRockAr",
    install_requires=[
        "beautifulsoup4",
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Internet",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Environment :: Console",
    ],
    zip_safe=False,
)
