from django.contrib import admin
from .models import Document, User, DocumentFile, Path
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')  # 'email'을 제거    
    fieldsets = (
        (None, {'fields': ('name','email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

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
