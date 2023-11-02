import os
import pickle
import pytest
from plex_sub_downloader.subliminalHelper import SubliminalHelper
from subliminal.video import Video
from subliminal.core import Language
from subliminal.subtitle import Subtitle

from vcr import VCR
import json
vcr = VCR(path_transformer=lambda path: path + '.yaml',
          record_mode=os.environ.get('VCR_RECORD_MODE', 'once'),
          match_on=['method', 'scheme', 'host', 'port', 'path', 'query', 'body'],
          cassette_library_dir=os.path.realpath(os.path.join('tests', 'cassettes', 'opensubtitles')))

@pytest.fixture
def subtitles():
    with open('tests/data/bbt_subs.pickle', 'rb') as fp:
        subtitles = pickle.load(fp)
        return subtitles

@vcr.use_cassette
def test_direct_search(movies):
    # Calling SubliminalHelper._search_videos() should return the same values in the same order as the requested languages. 
    sub = SubliminalHelper(providers=['opensubtitlesvip'], provider_configs={'opensubtitlesvip': {'username': 'python-plex-sub-downloader', 'password': 'plex-sub-downloader'}})

    man_of_steel = movies['man_of_steel']
    
    subtitles = sub._search_videos([man_of_steel], [['eng', 'fra', 'deu']])
    
    assert len(subtitles[man_of_steel]) == 3

    eng_lang = Language('eng')
    fra_lang = Language('fra')
    ger_lang = Language('deu')

    eng_sub = subtitles[man_of_steel][0]
    fra_sub = subtitles[man_of_steel][1]
    ger_sub = subtitles[man_of_steel][2]

    assert eng_sub.language == eng_lang
    assert fra_sub.language == fra_lang
    assert ger_sub.language == ger_lang

    assert eng_sub.id == "1953767330"
    assert fra_sub.id == "1953767650"
    assert ger_sub.id == "1953771409"


def test_filter_subtitles(movies):
    
    man_of_steel = movies['man_of_steel']

    sub = SubliminalHelper(providers=['opensubtitles'], format_priority=['str', 'smi'])

    subtitle = Subtitle(Language('eng'), False, None,)


