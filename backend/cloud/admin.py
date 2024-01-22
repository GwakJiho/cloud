from django.contrib import admin
from .models import Document, User, DocumentFile, Path

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ('name',)
  search_fields = ('name',)

@admin.register(Document)
class DocumnetAdmin(admin.ModelAdmin):
  list_display = ('title', 'publication_date', 'research_fund', 'writer')
  search_display = ('title', 'publication_date', 'research_fund', 'writer')

@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
  list_display = ('document',)
  search_display = ('document',)

@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
  list_display = ('current_path',)
  search_display = ('current_path',)
