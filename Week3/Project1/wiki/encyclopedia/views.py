from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, name):
    return render(request, "wiki/title.html", {
        "title": name.capitalize(),
        "entry": util.get_entry(name)
    })



# screwed something up with naming stuff wiki. 
# prolly have to rewatch some of hte lecture
# do 127.0.0.1:8000 to visit the index page, do /wiki/TITLE to get to the other page. Is it an app?
# why is the encyclopedia app index page viewable without any /encyclopedia? it was like that for other  apps