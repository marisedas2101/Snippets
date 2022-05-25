from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import auth

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


def edit_snippet(request, id):
    try:
        snippet = Snippet.objects.get(id=id)
        form = SnippetForm()
        if request.method == "POST":
            snippet.name = request.POST.get("name")
            snippet.code = request.POST.get("code")
            snippet.lang = request.POST.get("lang")
            snippet.save()
            return redirect("/")
        else:
            return render(request, "pages/edit.html", {"pagename": "Изменение сниппета", "snippet": snippet, "form": form})
    except ObjectDoesNotExist:
        return Http404("<h2>Snippet not found</h2>")


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect('index')
