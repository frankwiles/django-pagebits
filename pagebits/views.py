from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from .models import BitGroup, Page


class PageBitView(TemplateView):
    """
    Template view that adds PageBits to the Context
    """

    def get_template_name(self):
        if self.template_name:
            return [self.template_name]

        self.template_name = self.kwargs.get('template_name', None)

        if self.template_name is None:
            raise ImproperlyConfigured("PageBitView requires a template_name")
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super(PageBitView, self).get_context_data(**kwargs)
        new_context = {}

        for slug in self.group_slugs:
            group = BitGroup.objects.get_group(slug=slug)

            # Ensure we don't have slug/context name conflicts inside a single
            # view, which could happen if you define two slugs with the same
            # bit slugs.
            for bit in group.bits.all():
                new_context[bit.context_name] = bit.resolve()

        context.update(new_context)
        return context

    def get(self, request, *args, **kwargs):
        self.group_slugs = self.kwargs.pop('groups', None)

        if not self.group_slugs:
            raise ImproperlyConfigured(
                "PageBitViews require you to a 'groups' kwarg of PageGroup "
                "slugs so it knows which PageGroup Bits to load into this view."
            )

        self.get_template_name()
        context = self.get_context_data(**kwargs)
        return TemplateResponse(request, self.template_name, context)


class PageView(PageBitView):
    """
    View to display more generic "flatpages"
    """

    def get(self, request, *args, **kwargs):
        self.url = self.kwargs.pop('url', None)
        self.page = get_object_or_404(Page, url=self.url)

        self.group_slugs = [x.slug for x in self.page.bit_groups.all()]
        context = self.get_context_data(**kwargs)

        return TemplateResponse(request, self.page.template.path, context)

