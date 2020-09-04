from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util

import markdown2

from . import forms

import random

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
            "content": markdown2.markdown(entry), 'title': name
        })
    else:
        return render(request, "encyclopedia/pageNotFound.html")

def new_page(request):
    #if this is a POST request we need tovprocess the form data
    if request.method == 'POST':
        #create a form instace and populate it with data from the request:
        form = forms.NewPageForm(request.POST)
        #check ehether it's valid: 
        if form.is_valid():
            #process the data in form.cleaned_data as required 
            title = form.cleaned_data["titlePage"]
            content = form.cleaned_data["contentPage"]
            
            if util.get_entry(title):
                return render(request, "encyclopedia/newPage.html", {'form': form, 'exist':True} )
            else:
                util.save_entry(title, content)
                entry = util.get_entry(title)
                #redirec to new page:
                return render(request, "encyclopedia/page.html", {
                "content": markdown2.markdown(entry), "title": title
            
            })
                  
    #if a GET (or any other method) we'll create a blank form
    else:
        form = forms.NewPageForm()
        return render(request, "encyclopedia/newPage.html", {'form': form} )

def edit_page(request, name):
     
    if request.method == 'GET':
        entry = util.get_entry(name)

        data = {'contentPage': entry}
        form = forms.EditPageForm(data)

        if entry:
            return render(request, "encyclopedia/editPage.html", {
                'form': form, 'title': name
            })
        else:
            return render(request, "encyclopedia/pageNotFound.html")

    elif request.method == 'POST':
        form = forms.EditPageForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data["contentPage"]
            util.save_entry(name, content)
            entry = util.get_entry(name)
            #redirec to new URL:
            return render(request, "encyclopedia/page.html", {
                "content": markdown2.markdown(entry), 'title': name
            })
        else:
            return render(request, "encyclopedia/pageNotFound.html")
    else:
        return render(request, "encyclopedia/pageNotFound.html")

def random_page(request): 
     
    entrys = util.list_entries()
    numberEntrys = len(entrys)
    nameEntry = entrys[random.randrange(numberEntrys)]

    print(numberEntrys)
    return HttpResponseRedirect(nameEntry)