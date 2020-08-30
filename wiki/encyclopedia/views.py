from django.shortcuts import render

from . import util

import markdown2


def index(request):
    q = request.GET.get('q')

    if q:
        entry = util.get_entry(q)
        subEntry = util.get_sub_entry(q)
        if entry:
            return render(request, "encyclopedia/page.html", {
                "content": markdown2.markdown(entry)
            })
        elif subEntry:
            return render(request, "encyclopedia/index.html", {
                "entries": subEntry
            })
        else:
            return render(request, "encyclopedia/pageNotFound.html")
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def page(request, name):
    entry = util.get_entry(name)

    if entry:
        return render(request, "encyclopedia/page.html", {
            "content": markdown2.markdown(entry)
        })
    else:
        return render(request, "encyclopedia/pageNotFound.html")

def new_page(request):
     return render(request, "encyclopedia/newPage.html")