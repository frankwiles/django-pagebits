from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import BitGroup, PageBit, Page


class PageBitInline(admin.StackedInline):
    model = PageBit
    readonly_fields = ('created', 'modified')
    extra = 1

    fields = (
        'name',
        'context_name',
        'group',
        'type',
        'required',
        'order',
        'text_widget',
        'help_text',
        ('created', 'modified'),
    )


class BitGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    readonly_fields = ('created', 'modified')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PageBitInline]
    search_fields = ('name', 'slug', 'bits__name', 'bits__context_name')

    fields = (
        'name',
        'slug',
        ('created', 'modified'),
    )

    class Meta:
        model = BitGroup

admin.site.register(BitGroup, BitGroupAdmin)


class PageAdminForm(forms.ModelForm):
    """ Special form for editing a PageGroup's actual content """

    class Meta:
        model = Page
        exclude = (
            'name',
            'slug',
            'created',
            'modified',
        )

    def get_dynamic_fields(self, obj):
        fields = {}

        # Add our dynamic fields
        for bit in obj.bits.all():
            bit_key = 'bit_%s' % bit.pk

            if bit.type == 0:
                field = forms.CharField(
                    label=bit.name,
                    required=bit.required,
                    help_text=bit.help_text,
                    initial=bit.data.data,
                )

                if bit.text_widget == 'textarea':
                    field.widget = forms.Textarea()

            elif bit.type == 1:
                field = forms.CharField(
                    label=bit.name,
                    required=bit.required,
                    help_text=bit.help_text,
                    widget=CKEditorWidget(),
                    initial=bit.data.data,
                )
            elif bit.type == 2:
                field = forms.ImageField(
                    label=bit.name,
                    required=bit.required,
                    help_text=bit.help_text,
                    initial=bit.data.image,
                )

            fields[bit_key] = field

        return fields


class PageAdmin(admin.ModelAdmin):

    class Meta:
        model = Page

    def get_form(self, request, obj=None, **kwargs):
        admin_form = PageAdminForm()
        fields = admin_form.get_dynamic_fields(obj)
        form = type('PageAdminForm', (forms.ModelForm,), fields)
        return form

    def save_model(self, request, obj, form, change):
        """ Specially handle our slightly odd saving case """
        for key in form.cleaned_data.keys():
            if not key.startswith('bit_'):
                continue
            bit, pk = key.split('_')
            print "Saving pk: ", pk

            bit = PageBit.objects.get(pk=pk)
            if bit.type == 0 or bit.type == 1:
                print "setting data to: ", form.cleaned_data[key]
                bit.data.data = form.cleaned_data[key]
            else:
                bit.data.image = form.cleaned_data[key]
            bit.data.save()

    def has_add_permission(self, request):
        """ Don't allow users to add new PageData items, handled by signals """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Don't allow users to delete PageData items, handled by signals """
        return False

admin.site.register(Page, PageAdmin)
