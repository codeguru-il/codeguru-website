from django.shortcuts import redirect

from codeguru.views import error
from go.models import Link


def go(request, link: str):
    try:
        shortcut = Link.objects.get(name=link)
        return redirect(shortcut.url)
    except Link.DoesNotExist:
        return error(request, "Link not found")
