# Views.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from apoxz.xz.models import Page

def main(request):
    """Handle requests to the base URL of the xz app.
    
    This is basically a landing page.
    """
    pages = Page.objects.filter(parent__isnull=True, weight__gte=0).order_by('-weight')
    return render_to_response('landing.html', {pages: pages})

def page(request, slug):
    page = Page(slug=slug)