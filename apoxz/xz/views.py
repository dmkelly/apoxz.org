# Views.
from datetime import date
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from apoxz.xz.models import Page
from apoxz.xz import util

def main(request):
    """Handle requests to the base URL of the xz app.
    
    This is basically a landing page.
    """
    return render_to_response('landing.html', {'pages': util.main_nav()},
                              context_instance=RequestContext(request))

def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render_to_response('page.html', {
        'nav': util.main_nav(),
        'page': page,
        'child_pages': util.child_pages(parent=page)
    }, context_instance=RequestContext(request))