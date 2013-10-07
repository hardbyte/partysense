from django import forms
from django.utils.safestring import mark_safe
from django.template import Context, loader


class GoogleMapsWidget(forms.HiddenInput):

    def render(self, name, value, attrs=None, choices=()):
        self.attrs['base_point'] = self.attrs.get('base_point', "-43.532496,172.6343")
        self.attrs['width'] = self.attrs.get('width', 400)
        self.attrs['height'] = self.attrs.get('height', 400)

        t = loader.get_template("map_snippet.html")
        c = Context({
            'latitude': 'latitude_id',
            'longitude': 'longitude_id',
            'base_point': self.attrs['base_point'],
            'width': self.attrs['width'],
            'height': self.attrs['height'],
            'country_city': "Christchurch, New Zealand"
            })
        maps_html = t.render(c)

        rendered = super(GoogleMapsWidget, self).render(name, value, attrs)
        return rendered + mark_safe(maps_html)
