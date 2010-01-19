from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from doc_wiki.models import WikiPage


def wiki_index(request):
    """
    Renders a list of available wiki pages
    """
    pages = WikiPage.objects.all()
    
    return render_to_response("doc_wiki/index.html", {
        "pages": pages,
    }, context_instance=RequestContext(request))


def wiki_page(request, slug):
    """
    Tries to find a document matching the given slug, throws 404 if it can't
    """
    try:
        page = WikiPage.objects.get(slug=slug)
    except WikiPage.DoesNotExist:
        raise Http404
    
    return render_to_response("doc_wiki/page.html", {
        "page": page,
    }, context_instance=RequestContext(request))
