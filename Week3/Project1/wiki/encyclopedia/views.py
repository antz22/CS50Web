from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages

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

        entries = util.list_entries()
        for entry in entries:
            if title == entry:
                messages.error(request, 'This entry already exists.')
                return render(request, "encyclopedia/create.html")
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect('/wiki/%s/' % title)
# also fix thing with making sure it doesn't hvae existing entry/title


    return render(request, "encyclopedia/create.html")


def edit(request, name):
    entry = util.get_entry(name)

    if request.method == "POST":
        form = request.POST
        title = name
        content = form['content']
        util.save_entry(title, content)
        
        return HttpResponseRedirect('/wiki/%s/' % name)
    
    return render(request, "encyclopedia/edit.html", {
        "title": name,
        "entry": entry
    })
        # you don't need to convert markdown!!! u dum

def rand(request):
    entries = util.list_entries()
    name = random.choice(entries)
    return HttpResponseRedirect('/wiki/%s/' % name)