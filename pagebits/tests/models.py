from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import BitGroup, PageBit, PageData


class PageBitModelTests(TestCase):

    def test_uniqueness(self):
        group1 = BitGroup.objects.create(name='TestGroup1')
        group2 = BitGroup.objects.create(name='TestGroup2')

        PageBit.objects.create(name='header', type=0, group=group1)

        with self.assertRaises(ValidationError):
            PageBit.objects.create(name='header', type=0, group=group1)

        PageBit.objects.create(name='header', type=0, group=group2)

    def test_signals_work(self):
        group1 = BitGroup.objects.create(name='TestGroup1')
        bit1 = PageBit.objects.create(name='header', type=0, group=group1)
        bit2 = PageBit.objects.create(name='header2', type=0, group=group1)

        # Make sure PageData objects are created appropriately
        PageData.objects.get(bit=bit1)
        PageData.objects.get(bit=bit2)
