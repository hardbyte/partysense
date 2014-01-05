from partysense.music.models import Artist, Track, Genre

from django.contrib import admin


class TrackAdmin(admin.ModelAdmin):
    list_display = ("name", "artist", )


class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "track_count")


class GenreAdmin(admin.ModelAdmin):
    list_filter = ('popular', )
    ordering = ['name']
    search_fields = ['name', ]

admin.site.register(Genre, GenreAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Artist, ArtistAdmin)
