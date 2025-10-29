from django import template
from django.conf import settings

register = template.Library()

@register.filter
def icon_url_display(url):
    if not url:
        return ''
    url = str(url)
    # github blob 連結自動轉 raw
    if 'github.com' in url and '/blob/' in url:
        url = url.replace('/blob/', '/raw/')
    elif not url.startswith('http') and not url.startswith('/'):
        url = settings.MEDIA_URL + url
    return url
