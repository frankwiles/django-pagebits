from django.core.exceptions import ImproperlyConfigured
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from .exceptions import PageBitNameClash
from .models import PageGroup


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
            group = PageGroup.objects.select_related(
                'bits',
                'bits__data',
            ).get(slug=slug)

            # Ensure we don't have slug/context name conflicts inside a single
            # view, which could happen if you define two slugs with the same
            # bit slugs.
            for bit in group.bits.all():
                if bit.slug in new_context:
                    raise PageBitNameClash(
                        "Bit with slug/context name '%s' already exists "
                        "in this view."
                    )
                else:
                    new_context[bit.slug] = bit.resolve()

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
