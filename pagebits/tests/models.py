from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.safestring import SafeText

from ..models import BitGroup, PageBit, PageData


class PageBitModelTests(TestCase):

    def setUp(self):
        self.group1 = BitGroup.objects.create(name='TestGroup1')
        self.bit1 = PageBit.objects.create(
            name='header',
            context_name='header',
            type=PageBit.PLAIN_TEXT,
            group=self.group1
        )
        self.bit2 = PageBit.objects.create(
            name='header2',
            context_name='header2',
            type=PageBit.PLAIN_TEXT,
            group=self.group1
        )

    def test_uniqueness(self):
        group2 = BitGroup.objects.create(name='TestGroup2')

        with self.assertRaises(ValidationError):
            PageBit.objects.create(
                name='header',
                context_name='header',
                type=PageBit.PLAIN_TEXT,
                group=self.group1
            )

        PageBit.objects.create(
            name='header',
            context_name='header',
            type=PageBit.PLAIN_TEXT,
            group=group2
        )

    def test_signals_work(self):
        # Make sure PageData objects are created appropriately
        PageData.objects.get(bit=self.bit1)
        PageData.objects.get(bit=self.bit2)

    def test_manager_caching(self):
        """ Test that our manager caches appropriately """
        with self.assertNumQueries(3):
            BitGroup.objects.get_group('testgroup1')

        with self.assertNumQueries(0):
            BitGroup.objects.get_group('testgroup1')

    def test_resolve(self):
        bit3 = PageBit.objects.create(
            name='markup',
            context_name='markup',
            type=PageBit.HTML,
            group=self.group1
        )

        self.assertFalse(isinstance(self.bit1.resolve(), SafeText))
        self.assertFalse(isinstance(self.bit2.resolve(), SafeText))
        self.assertTrue(isinstance(bit3.resolve(), SafeText))
