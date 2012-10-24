from apoxz.xz import models
from django.contrib import admin

class PageAdmin(admin.ModelAdmin):
    """Specify which Page fields should be exposed in the admin console.
    
    More specifically, hide the slug field because we want to auto-generate
    this value.
    """
    fields = ['parent', 'title', 'hide_date', 'show_date',
        'sub_title', 'content', 'weight']
    # readonly_fields = ('show_date',)

class GalleryAdmin(admin.ModelAdmin):
    fields = ['title', 'description']

class GalleryImageAdmin(admin.ModelAdmin):
    fields = ['gallery', 'title', 'description']

class LinkAdmin(admin.ModelAdmin):
    fields = ['title', 'href', 'weight']

admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Gallery, GalleryAdmin)
admin.site.register(models.GalleryImage, GalleryImageAdmin)
admin.site.register(models.Link, LinkAdmin)
