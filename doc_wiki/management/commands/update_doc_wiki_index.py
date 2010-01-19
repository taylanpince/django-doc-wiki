import os
import re

from optparse import make_option

from django.core.management.base import BaseCommand

from doc_wiki import settings
from doc_wiki.models import WikiPage


class Command(BaseCommand):
    """
    Update Doc Wiki index
    """
    option_list = BaseCommand.option_list + (
        make_option("--update-git", "-g", action="store_true", dest="update_git", help="Pull from Git repo before updating the index"),
    )

    def handle(self, **options):
        update_git = options.get("username", False)

        if update_git:
            pass

        for file_name in os.listdir(settings.DIRECTORY_PATH):
            path = os.path.join(settings.DIRECTORY_PATH, file_name)

            if os.path.isfile(path):
                page = WikiPage.objects.get_or_create(slug=file_name)
                print page

