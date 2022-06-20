from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic.list import ListView

from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from MainApp.models import Snippet


class SnippetList(ListView):

    model = Snippet
    template_name = 'pages/view_snippets.html'
    context_object_name = 'snippets'
    extra_context = {'pagename': 'Просмотр сниппетов'}

    def get_queryset(self):
        if 'filter' in self.request.GET:
            filter_val = self.model.objects.filter(user=self.request.user)
            return filter_val
        return self.model.objects.all()


def index_page(request):
    snippets = None
    method = 'get'
    if request.method == 'POST':
        num_snippet = request.POST.get('number')
        snippets = Snippet.objects.filter(pk=num_snippet)
        method = 'post'
    context = {'pagename': 'PythonBin', 'snippets': snippets, "method": method}
    return render(request, 'pages/index.html', context)



def add_snippet_page(request):
    if request.method == 'GET':
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', 'form': form}
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            # commit=False- мы получаем объект snippet, но сохранения в БД не происходит
            snippet = form.save(commit=False)
            snippet.user = request.user
            # а здесь уже происходит сохранение в БД
            snippet.save()
            return redirect("list")


# def snippets_page(request):
#     template = 'pages/view_snippets.html'
#     if request.method == "GET":
#         snippets = Snippet.objects.all()
#         context = {'pagename': 'Просмотр сниппетов', 'snippets': snippets}
#         if 'filter' in request.GET:
#             snippets = Snippet.objects.filter(user=request.user)
#             context = {'pagename': 'Просмотр сниппетов', 'snippets': snippets}
#             return render(request, template, context)
#         return render(request, template, context)


def snippet_page(request, id):
    try:
        sn = Snippet.objects.get(pk=id)
        form = CommentForm()
        context = {'snippet': sn, "pagename": "Детали сниппета", "comment_form": form}
        return render(request, 'pages/snippet_page.html', context)
    except ObjectDoesNotExist:
        raise Http404(f"Сниппета c id={id} не существует")


@login_required()
def delete(request, id):
    try:
        sn = Snippet.objects.get(id=id)
        sn.delete()
        return redirect("list")
    except ObjectDoesNotExist:
        return Http404("<h2>Snippet not found</h2>")


@login_required()
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
    return redirect(request.META.get('HTTP_REFERER', '/'))


def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def register(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {"pagename": "Регистрация пользователя", "form": form}
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        context = {"pagename": "Регистрация пользователя", "form": form}
        return render(request, "pages/registration.html", context)


def comment_add(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        snippet_id = request.POST.get('snippet_id')
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snippet_id)
            comment.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    raise Http404
