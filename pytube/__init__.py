# -*- coding: utf-8 -*-
# flake8: noqa: F401
# noreorder
"""
Pytube: a very serious Python library for downloading YouTube Videos.
"""
__title__ = "pytube"
__author__ = "Kaiser Pister"
__license__ = "MIT License"
__copyright__ = "Copyright 2020 Kaiser Pister"

from pytube.version import __version__
from pytube.streams import Stream
from pytube.captions import Caption
from pytube.query import CaptionQuery
from pytube.query import StreamQuery
from pytube.__main__ import YouTube
from pytube.contrib.playlist import Playlist
