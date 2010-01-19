import os

from django.conf import settings


DIRECTORY_PATH = getattr(settings, "DOC_WIKI_DIRECTORY_PATH", os.path.join(os.path.realpath(os.path.dirname(__file__)), 'docs/'))
FILE_PATH_RE = getattr(settings, "DOC_WIKI_FILE_PATH_RE", r"*\.txt")