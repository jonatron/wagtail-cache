"""
Views for the wagtail admin dashboard.
"""

from django.core.cache import caches
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from wagtailcache.cache import clear_cache
from wagtailcache.settings import wagtailcache_settings


def index(request):
    """
    The wagtail-cache admin panel.
    """
    # Get the keyring to show cache contents.
    _wagcache = caches[wagtailcache_settings.WAGTAIL_CACHE_BACKEND]

    # needs to be redis
    # pip install redis
    # docker run -p 6379:6379 redis

    paths = []
    scan_key = _wagcache.make_and_validate_key("WCPth*")
    prefix = _wagcache.make_and_validate_key("")
    prefix_len = len(prefix) + len("WCPth")
    # todo add a limit
    for key in _wagcache._cache.get_client().scan_iter(scan_key):
        paths.append(key[prefix_len:].decode("ascii"))

    return render(
        request,
        "wagtailcache/index.html",
        {
            "paths": paths,
        },
    )


def clear(request):
    """
    Clear the cache and redirect back to the admin settings page.
    """
    clear_cache()
    return HttpResponseRedirect(reverse("wagtailcache_admin:index"))
