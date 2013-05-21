from partysense.music.models import Artist, Track

from django.contrib import admin

class TrackAdmin(admin.ModelAdmin):
    list_display = ("name", "artist", )


class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "track_count")


admin.site.register(Track, TrackAdmin)
admin.site.register(Artist, ArtistAdmin)
