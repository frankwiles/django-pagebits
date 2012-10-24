from django.contrib import admin
#from django import forms

from .models import PageGroup, PageBit, PageData


class PageBitInline(admin.StackedInline):
    model = PageBit
    readonly_fields = ('created', 'modified')
    prepopulated_fields = {'slug': ('name',)}

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

    fields = (
        'name',
        'slug',
        ('created', 'modified'),
    )

    class Meta:
        model = PageGroup

admin.site.register(PageGroup, PageGroupAdmin)


class PageDataAdmin(admin.ModelAdmin):

    class Meta:
        model = PageData

admin.site.register(PageData, PageDataAdmin)
