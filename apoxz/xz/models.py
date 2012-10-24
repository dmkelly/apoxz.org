from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify

class Page(models.Model):
    """A Page represents a single page on the site.
    
    To handle navigation logic, each Page must belong to a single category.
    """
    weight = models.IntegerField(default=-1,
        help_text='Descending order in which the links are displayed on' +
            ' the navigation. An index < 0 is hidden.')
    parent = models.ForeignKey('self', null=True, blank=True,
        help_text='If set, this page will become a sub-page of the parent to' +
        ' allow multi-level navigation.')
    title = models.CharField(max_length=36, unique=True,
        help_text='User-friendly title for the page.')
    slug = models.SlugField(max_length=36, unique=True)
    date_modified = models.DateField(auto_now=True)
    hide_date = models.DateField(blank=True, null=True, help_text='If set, the date to ' +
        'stop displaying this page on the site. Allows ability to ' +
        'automatically hide stale content.')
    show_date = models.DateField(default=datetime.now, help_text='If set, the date ' +
        'to start displaying this page on the site. Allows ability to ' +
        'automatically create new content before it needs to be published.')
    sub_title = models.CharField(max_length=72, null=True, blank=True,
        help_text='Optional - a supporting sub-title.')
    content = models.CharField(null=True, blank=True, max_length=4096,
        help_text='The main content of the page.')
#    image = models.ImageField('Page Image', upload_to='pages/', blank=True, null=True)
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Extends the default save functionality to automatically slugify the
        slug field based on the title.
        """
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

class Gallery(models.Model):
    """A Gallery represents a collection of related images.
    
    Each Gallery should contain one or more images.
    """
    title = models.CharField(max_length=36, unique=True,
        help_text='User-friendly title for the gallery.')
    slug = models.SlugField(max_length=36, unique=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    description = models.CharField(max_length=512, null=True, blank=True,
        help_text='A brief description of the gallery.')
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Extends the default save functionality to automatically slugify the
        slug field based on the title.
        """
        self.slug = slugify(self.title)
        super(Gallery, self).save(*args, **kwargs)

class GalleryImage(models.Model):
    """A GalleryImage represents a single image within a gallery.
    
    """
    gallery = models.ForeignKey(Gallery,
        help_text='The gallery that this image belongs to.')
    title = models.CharField(max_length=36,
        help_text='User-friendly title for the image.')
    slug = models.SlugField(max_length=36)
    description = models.CharField(max_length=160, null=True, blank=True,
        help_text='A brief description of the image.')
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Extends the default save functionality to automatically slugify the
        slug field based on the title.
        """
        self.slug = slugify(self.title)
        super(GalleryImage, self).save(*args, **kwargs)
    
    class Meta:
        unique_together = ('gallery', 'slug')

class Link(models.Model):
    """A Link represents a hyperlink to a website recommended by APO-XZ.
    
    It will appear on the Links page, ordered by weight.
    """
    weight = models.IntegerField(help_text='Determines how links are ordered' +
        ' on the page. Links are ordered in descending order. Links with a ' +
        'weight < 0 are hidden.')
    title = models.CharField(max_length=36, unique=True,
        help_text='User-friendly title for the image.')
    slug = models.SlugField(max_length=36, unique=True)    # Allows us to use
        # images for the links if we want, something like:
        #     {% MEDIA_URL %}/link/{% link.slug %}.jpg
    href = models.URLField(max_length=255, unique=True,
        help_text='The absolute URL of the link. Should probably start with ' +
        '"http://"')
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Extends the default save functionality to automatically slugify the
        slug field based on the title.
        """
        self.slug = slugify(self.title)
        super(Link, self).save(*args, **kwargs)