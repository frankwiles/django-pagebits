from django.core.exceptions import ImproperlyConfigured
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from .exceptions import PageBitNameClash
from .models import PageGroup


class PageBitView(TemplateView):
    """
    Template view that adds PageBits to the Context
    """

    def get_context_data(self, **kwargs):
        context = super(PageBitView, self).get_context_data(**kwargs)
        new_context = {}

        for slug in self.group_slugs:

            group = PageGroup.objects.select_related(
                'bits',
                'bits__data',
            ).get(slug=slug)

            for bit in group.bits.all():
                if bit.slug in new_context:
                    raise PageBitNameClash(
                        "Bit with slug/context name '%s' already exists "
                        "in this view."
                    )
                else:
                    new_context[bit.slug] = bit.resolve()

        return context

    def get(self, request, *args, **kwargs):
        self.group_slugs = self.kwargs.pop('groups', None)

        if not self.group_slugs:
            raise ImproperlyConfigured(
                "PageBitViews require you to a 'groups' kwarg of PageGroup "
                "slugs so it knows which PageGroup Bits to load into this view."
            )

        context = self.get_context_data(**kwargs)
        return TemplateResponse(request, self.template_name, context)
