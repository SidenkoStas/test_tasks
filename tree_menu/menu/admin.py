from django.contrib import admin
from .models import Menu, Section


class SectionAdmin(admin.ModelAdmin):
    list_display = ("title", "parent", "menu")
    prepopulated_fields = {"slug": ("title", )}


class MenuAdmin(admin.ModelAdmin):
    list_display = ("title", )
    prepopulated_fields = {"slug": ("title", )}


admin.site.register(Section, SectionAdmin)
admin.site.register(Menu, MenuAdmin)
