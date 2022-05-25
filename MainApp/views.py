from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect

from MainApp.forms import SnippetForm
from MainApp.models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == 'GET':
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', 'form': form}
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list")


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', 'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)


def snippet_page(request, id):
    try:
        sn = Snippet.objects.get(pk=id)
        return render(request, 'pages/snippet_page.html', context={'snippet': sn})
    except ObjectDoesNotExist:
        raise Http404(f"Сниппета c id={id} не существует")


def delete(request, id):
    try:
        sn = Snippet.objects.get(id=id)
        sn.delete()
        return redirect("list")
    except ObjectDoesNotExist:
        return Http404("<h2>Snippet not found</h2>")
