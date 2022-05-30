from django.contrib import admin
from MainApp.models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('name', 'lang', 'code', 'creation_date', 'user')


admin.site.register(Snippet, SnippetAdmin)
