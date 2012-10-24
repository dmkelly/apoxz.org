from apoxz.xz.models import Page
from datetime import date
from django.db.models import Q

def main_nav():
    today = date.today()
    return Page.objects.filter(
        parent__isnull=True,    # Only want root-level pages for front page.
        weight__gte=0,          # Only want visible pages.
        show_date__lte=today    # Make sure page can be published.
    ).filter(
        Q(hide_date__gt=today) | Q(hide_date__isnull=True) # Make sure page hasn't expired.
    ).order_by('-weight')       # Follow defined order.