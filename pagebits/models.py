from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe

from .managers import BitGroupManager
from .utils import bitgroup_cache_key

BIT_TYPE_CHOICES = (
    (0, 'Plain Text'),
    (1, 'HTML'),
    (2, 'Image'),
)


class BitGroup(models.Model):
    """ A Page Group, which can be used on more than one logical page """
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField()

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    objects = BitGroupManager()

    class Meta:
        verbose_name = 'Bit Group'
        verbose_name_plural = 'Bit Groups'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Slugify if does not exist on first save
        if not self.pk and not self.slug:
            self.slug = slugify(self.name)

        self.modified = timezone.now()

        super(BitGroup, self).save(*args, **kwargs)


class Page(BitGroup):
    """ Proxy model to allow special admin interface """

    class Meta:
        proxy = True


TEXT_WIDGET_CHOICES = (
    ('charfield', 'Text Input Field'),
    ('textarea', 'Textarea Input Field'),
)


class PageBit(models.Model):
    """
    A PageBit stores the sensitive data about a Bit, what type of data it can
    handle.  This allows permissions to be given to some users to add/edit bits,
    and others only the ability to edit the actual data.
    """
    type = models.IntegerField('Bit Type', choices=BIT_TYPE_CHOICES, default=0)
    group = models.ForeignKey(BitGroup, related_name='bits')
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField(
        unique=False,
        help_text="This will be the name in the template context."
    )
    order = models.IntegerField('Admin form display order', default=1)

    text_widget = models.CharField(
        max_length=10,
        choices=TEXT_WIDGET_CHOICES,
        default='charfield',
        help_text="Which type of input widget to use in admin form",
    )

    required = models.BooleanField(
        'Required',
        default=False,
        help_text='Is this field required?'
    )

    help_text = models.TextField('Optional admin help text', blank=True)

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('order', 'created')

    def __unicode__(self):
        return self.name

    def clean(self):
        # Ensure our slug and group__slug are unique together

        qs = self.__class__._default_manager.filter(
            group__slug=self.group.slug,
            slug=self.slug
        )

        # Exclude ourself in checking for duplicate slugs
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError(
                "The slug '%s' is already used in PageGroup '%s'" % (self.slug, self.group.name)
            )

    def save(self, *args, **kwargs):
        # Slugify if does not exist on first save
        if not self.pk and not self.slug:
            self.slug = slugify(self.name)

        self.modified = timezone.now()
        self.full_clean()

        super(PageBit, self).save(*args, **kwargs)

    def resolve(self):
        if self.type == 0:
            # Handle simple plain text returns
            return self.data.data
        elif self.type == 1:
            # Mark HTML data safe to avoid escaping it in views
            return mark_safe(self.data.data)
        elif self.type == 2:
            # Return the actual image itself
            return self.data.image


@receiver(post_save, sender=PageBit)
def create_page_data(sender, instance, created, **kwargs):
    # Create PageData items on creation
    if created:
        PageData.objects.create(bit=instance)

    # Bust the BitGroup cache
    key = bitgroup_cache_key(instance.slug)
    cache.delete(key)


class PageData(models.Model):
    bit = models.OneToOneField(PageBit, related_name='data')
    data = models.TextField(blank=True)
    image = models.ImageField(upload_to='pagebits/data/images/', blank=True, null=True)

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "%s - %s (%s)" % (
            self.bit.group.name,
            self.bit.name,
            self.bit.slug
        )

    class Meta:
        verbose_name = 'Page Data'
        verbose_name_plural = 'Page Data'

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(PageData, self).save(*args, **kwargs)
