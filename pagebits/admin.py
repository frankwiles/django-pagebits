from django.contrib import admin
#from django import forms

from .models import PageGroup, PageBit, PageData


class PageBitInline(admin.StackedInline):
    model = PageBit
    readonly_fields = ('created', 'modified')
    prepopulated_fields = {'slug': ('name',)}
    extra = 1

    fields = (
        'name',
        'slug',
        'group',
        'type',
        'use_charfield_widget',
        'use_textarea_widget',
        'help_text',
        ('created', 'modified'),
    )


class PageGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    readonly_fields = ('created', 'modified')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PageBitInline]
    search_fields = ('name', 'slug', 'bits__name', 'bits__slug')

    fields = (
        'name',
        'slug',
        ('created', 'modified'),
    )

    class Meta:
        model = PageGroup

admin.site.register(PageGroup, PageGroupAdmin)


class PageDataAdmin(admin.ModelAdmin):
    readonly_fields = ('bit', 'created', 'modified')

    fields = (
        'bit',
        'data',
        'image',
        ('created', 'modified'),
    )

    class Meta:
        model = PageData

    def has_add_permission(self, request):
        """ Don't allow users to add new PageData items, handled by signals """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Don't allow users to delete PageData items, handled by signals """
        return False

admin.site.register(PageData, PageDataAdmin)
