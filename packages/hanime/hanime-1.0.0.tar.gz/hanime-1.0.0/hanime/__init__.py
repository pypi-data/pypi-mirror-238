from requests import get
from .search import *
from .video import *
from .image import *
from .user import *

__title__: str = 'hanime'
__author__: str = 'cxstles'
__version__: str = '1.0.0'

VERSION: str = get('https://pypi.org/pypi/hanime/json').json()['info']['version']
if VERSION != __version__:
    print('hanime | New Version | pip install -U hanime')
