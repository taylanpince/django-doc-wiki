from django.core.cache import cache
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from doc_wiki import settings
from doc_wiki.managers import WikiPageManager
from doc_wiki.parsers import parse_markdown


class WikiPage(models.Model):
    """
    A wiki page based on a document in the file system
    """
    slug = models.SlugField(_("Slug"), max_length=255)
    path = models.FilePathField(_("Path"), path=settings.DIRECTORY_PATH, recursive=False, max_length=255)
    content = models.TextField(_("Content"), blank=True)
    timestamp = models.DateTimeField(_("Time Stamp"), auto_now=True)

    admin_objects = models.Manager()
    objects = WikiPageManager()

    class Meta:
        verbose_name = _("Wiki Page")
        verbose_name_plural = _("Wiki Pages")

    def __unicode__(self):
        return u"Wiki Page: %s" % self.slug

    @models.permalink
    def get_absolute_url(self):
        return ("doc_wiki_page", (), {
            "slug": self.slug,
        })

    @property
    def content_html(self):
        """
        Parses the content field using markdown and pygments, caches the results
        """
        key = "wiki_pages_content_%d" % self.pk
        html = cache.get(key)

        if not html:
            html = parse_markdown(self.content)
            cache.set(key, html, 60 * 60 * 24 * 30)

        return mark_safe(html)

    def save(self):
        if self.pk:
            cache.delete("wiki_pages_content_%d" % self.pk)

        super(WikiPage, self).save()
