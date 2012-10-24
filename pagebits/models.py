from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe

BIT_TYPE_CHOICES = (
    (0, 'Plain Text'),
    (1, 'HTML'),
    (2, 'Image'),
)


class PageGroup(models.Model):
    """ A Page Group, which can be used on more than one logical page """
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField()

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Page Group'
        verbose_name_plural = 'Page Groups'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Slugify if does not exist on first save
        if not self.pk and not self.slug:
            self.slug = slugify(self.name)

        self.modified = timezone.now()

        super(PageGroup, self).save(*args, **kwargs)


class PageBit(models.Model):
    """
    A PageBit stores the sensitive data about a Bit, what type of data it can
    handle.  This allows permissions to be given to some users to add/edit bits,
    and others only the ability to edit the actual data.
    """
    type = models.IntegerField('Bit Type', choices=BIT_TYPE_CHOICES, default=0)
    group = models.ForeignKey(PageGroup, related_name='bits')
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField(
        unique=False,
        help_text="This will be the name in the template context."
    )

    use_charfield_widget = models.BooleanField(default=True)
    use_textarea_widget = models.BooleanField(default=False)

    help_text = models.TextField('Optional admin help text', blank=True)

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    def clean(self):
        # Ensure our slug and group__slug are unique together

        qs = self.__class__._default_manager.filter(
            group__slug=self.group.slug,
            slug=self.slug
        )

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


# Connect post save signal to create PageData items
@receiver(post_save, sender=PageBit)
def create_page_data(sender, instance, created, **kwargs):
    if created:
        PageData.objects.create(bit=instance)


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

    def clean(self):
        # Ensure we have the proper data for our PageBit type
        if self.bit.type == 2:
            if not self.image:
                raise ValidationError("No image entered for image type.")
        else:
            if not self.data:
                raise ValidationError("No text entered for text type")

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(PageData, self).save(*args, **kwargs)
