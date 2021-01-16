from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import random
from markdown2 import Markdown

from . import util

class NewForm(forms.Form):
    name = forms.CharField(label="Search Encyclopedia")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    if util.get_entry(name):
        entry = util.get_entry(name)
        markdowner = Markdown()
        return render(request, "encyclopedia/wiki.html", {
            "title": name,
            "entry": markdowner.convert("%s" % entry)
        })
    else:
        return render(request, "encyclopedia/error.html")
   

def search(request):
    if request.method == "POST":
        form = request.POST
        name = form['q']
        if util.get_entry(name):
            return HttpResponseRedirect('/wiki/%s/' % name)
            # how to deal with capitalization and stuff?
        else:
            return render(request, "encyclopedia/search.html", {
                "entries": util.list_entries(),
                "substr": name
            })

def create(request):
    if request.method == "POST":
        form = request.POST
        title = form['title']
        content = form['content']
        util.save_entry(title, content)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
# probably have to look over this again. the notpython entry markdown is all screwed up.

    return render(request, "encyclopedia/create.html")


# def edit(request):
#   if request.method == "POST":
#       return render(request, "encyclopedia/wiki.html", {
                # TODO
#       })


def rand(request):
    entries = util.list_entries()
    name = random.choice(entries)
    return HttpResponseRedirect('/wiki/%s/' % name)