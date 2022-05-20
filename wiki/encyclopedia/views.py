import random
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from markdown2 import Markdown
from . import util



class NewEntry(forms.Form):
    #Class for new entries
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "placeholder": "Entry Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={}))

class Edit(forms.Form):
  #Class for editing entries
  text = forms.CharField(label='', widget=forms.Textarea(attrs={}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()})

def entry(request, title):
    getEntry = util.get_entry(title)
    if getEntry is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,"message": "Entry doesn't exist" 
            })
         
    else:
        # Title exists, convert md to HTML 
        markdown = Markdown().convert(getEntry)
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown,
            "title": title
            })

def search(request):
  value = request.GET.get('q','')
  if(util.get_entry(value) is not None):
    return redirect(reverse('entry', args=[value]))  
  
  associated = []
  for entry in util.list_entries():
      if value.lower() in entry.lower():
        associated.append(entry)
        return render(request, "encyclopedia/index.html",{
        "entries": associated,
        "search": True,
        "value": value
    })

  else:
    return render(request, "encyclopedia/index.html",{
        "entries": util.list_entries,
        "search": True,
        "value": value
    })


def newEntry(request):
    #  Access by link
    if request.method == "GET":
        return render(request, "encyclopedia/newEntry.html", {
          "new_entry": NewEntry()})

    # Access by submission:
    elif request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
          title = form.cleaned_data['title']
          cleanText = form.cleaned_data['text']
          entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/error.html", {
               "message": "Entry already exist"
            })
            
        else:
            util.save_entry(title,cleanText)
            return redirect(reverse('entry', args=[title]))


def edit(request, title):
    
    # Access by link
    if request.method == "GET":
        getEntry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
          "title": title,
          "edit_form": Edit(initial={'text':getEntry}),
        })
        
    # Access by Post
    elif request.method == "POST":
        form = Edit(request.POST)

        if form.is_valid():
          cleanText = form.cleaned_data['text']
          util.save_entry(title, cleanText)
          return redirect(reverse('entry', args=[title]))

        else:
          return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit": form,
          })

def random_title(request):
    title = random.choice(util.list_entries())
    return redirect(reverse('entry', args=[title]))


