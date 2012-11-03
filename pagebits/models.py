from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .managers import BitGroupManager
from .utils import bitgroup_cache_key


class BitGroup(models.Model):
    """ A Page Group, which can be used on more than one logical page """
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField()
    description = models.TextField(
        blank=True,
        help_text=_("Description show in the admin"),
    )
    instructions = models.TextField(
        blank=True,
        help_text=_("Detailed instructions presented at top of the admin form."),
    )
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    objects = BitGroupManager()

    class Meta:
        verbose_name = _('Bit Group')
        verbose_name_plural = _('Bit Groups')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Slugify if does not exist on first save
        if not self.pk and not self.slug:
            self.slug = slugify(self.name)

        self.modified = timezone.now()

        super(BitGroup, self).save(*args, **kwargs)


class PageEdit(BitGroup):
    """ Proxy model to allow special admin interface """

    class Meta:
        verbose_name = _('Edit Page Data')
        verbose_name_plural = _('Edit Page Data')
        proxy = True


class PageBit(models.Model):
    """
    A PageBit stores the sensitive data about a Bit, what type of data it can
    handle.  This allows permissions to be given to some users to add/edit bits,
    and others only the ability to edit the actual data.
    """
    PLAIN_TEXT = 0
    HTML = 1
    IMAGE = 2
    BIT_TYPE_CHOICES = (
        (PLAIN_TEXT, 'Plain Text'),
        (HTML, 'HTML'),
        (IMAGE, 'Image'),
    )

    type = models.IntegerField(_('Bit Type'), choices=BIT_TYPE_CHOICES, default=0)
    group = models.ForeignKey(BitGroup, related_name='bits')
    name = models.CharField(_('Name'), max_length=100)
    context_name = models.CharField(
        max_length=100,
        help_text=_("This will be the name in the template context."),
    )
    order = models.IntegerField(_('Admin form display order'), default=1)

    WIDGET_CHARFIELD = 'charfield'
    WIDGET_TEXTAREA = 'textarea'
    TEXT_WIDGET_CHOICES = (
        (WIDGET_CHARFIELD, _('Text Input Field')),
        (WIDGET_TEXTAREA, _('Textarea Input Field')),
    )

    text_widget = models.CharField(
        max_length=10,
        choices=TEXT_WIDGET_CHOICES,
        default='charfield',
        help_text=_("Which type of input widget to use in admin form for Plain Text fields."),
    )

    required = models.BooleanField(
        _('Required'),
        default=False,
        help_text=_('Is this field required?')
    )

    help_text = models.TextField(_('Optional admin help text'), blank=True)

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('order', 'created')

    def __unicode__(self):
        return self.name

    def clean(self):
        # Ensure our context_name and group__slug are unique together

        qs = self.__class__._default_manager.filter(
            group__slug=self.group.slug,
            context_name=self.context_name
        )

        # Exclude ourself in checking for duplicates
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError(
                "The name '%s' is already used in PageGroup '%s'" % (self.context_name, self.group.name)
            )

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        self.full_clean()

        super(PageBit, self).save(*args, **kwargs)

    def resolve(self):
        if self.type == self.PLAIN_TEXT:
            # Handle simple plain text returns
            return self.data.data
        elif self.type == self.HTML:
            # Mark HTML data safe to avoid escaping it in views
            return mark_safe(self.data.data)
        elif self.type == self.IMAGE:
            # Return the actual image itself
            return self.data.image


@receiver(post_save, sender=PageBit)
def create_page_data(sender, instance, created, **kwargs):
    """ Handle automatically creating PageData items on creation """
    # Do nothing if we're loading a fixture
    if kwargs.get('raw', False):
        return

    if created:
        PageData.objects.create(bit=instance)

    # Bust the BitGroup cache
    key = bitgroup_cache_key(instance.context_name)
    cache.delete(key)


class PageData(models.Model):
    bit = models.OneToOneField(PageBit, related_name='data')
    data = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='pagebits/data/images/',
        blank=True,
        null=True
    )

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "%s - %s (%s)" % (
            self.bit.group.name,
            self.bit.name,
            self.bit.context_name,
        )

    class Meta:
        verbose_name = _('Page Data')
        verbose_name_plural = _('Page Data')

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(PageData, self).save(*args, **kwargs)


class PageTemplate(models.Model):
    """ Associate Template names to filesystem paths """
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('Name shown to user'),
    )

    path = models.CharField(
        _('Path'),
        max_length=200,
        help_text=_("Path to template in TEMPLATE_DIRS, for example 'pages/homepage.html'"),
    )

    class Meta:
        verbose_name = _('Page Template')
        verbose_name_plural = _('Page Template')
        ordering = ('name', )


class Page(models.Model):
    """ Model to represent an automatic 'flatpage' """
    name = models.CharField(_('Name'), max_length=100)
    url = models.CharField(
        _('URL'),
        max_length=200,
        help_text=_("Define the URL for this page, for example 'about/'. NOTE: You should not include the initial slash."),
        db_index=True,
    )
    template = models.ForeignKey(PageTemplate, related_name='pages')
    bit_groups = models.ManyToManyField(BitGroup, related_name='pages')

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ('name', )

