# Views.
from datetime import date
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from apoxz.xz.models import Page

def main(request):
    """Handle requests to the base URL of the xz app.
    
    This is basically a landing page.
    """
    today = date.today()
    pages = Page.objects.filter(
#            parent__isnull=True,    # Only want root-level pages for front page.
            weight__gte=0,          # Only want visible pages.
#            show_date__lte=today    # Make sure page can be published.
        ).filter(
#            Q(hide_date__gt=today) | Q(hide_date__isnull=True) # Make sure page hasn't expired.
        ).order_by('-weight')       # Follow defined order.
    return render_to_response('landing.html', {pages: pages})

def page(request, slug):
    page = Page(slug=slug)