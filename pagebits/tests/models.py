from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import PageGroup, PageBit, PageData


class PageBitModelTests(TestCase):

    def test_uniqueness(self):
        group = PageGroup.objects.create(name='TestGroup')

        bit1 = PageBit.objects.create(name='header', type=0, group=group)

        with self.assertRaises(ValidationError):
            bit2 = PageBit.objects.create(name='header', type=0, group=group)
