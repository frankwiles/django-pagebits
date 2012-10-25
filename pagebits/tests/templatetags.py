import os
import shutil

from django.core.files import File
from django.core.cache import cache
from django.conf import settings
from django.test import TestCase

from ..models import BitGroup, PageBit
from ..templatetags.pagebits import pagebits


class PageBitTemplateTagTests(TestCase):

    def setUp(self):
        self.group = BitGroup.objects.create(name='testgroup')
        self.bit1 = PageBit.objects.create(
            name='header',
            type=0,
            group=self.group
        )
        self.bit1.data.data = 'Test Page Header'
        self.bit1.data.save()

        self.bit2 = PageBit.objects.create(
            name='page-block',
            type=1,
            group=self.group
        )

        self.bit2.data.data = '<p>Block</p>'
        self.bit2.data.save()

        self.bit3 = PageBit.objects.create(
            name='logo-image',
            type=2,
            group=self.group
        )
        f = open(os.path.join(os.path.dirname(__file__), 'test-image.jpg'))
        myfile = File(f)

        self.bit3.data.image = myfile
        self.bit3.data.save()

    def test_templatetag(self):
        bits = pagebits('testgroup')
        self.assertEqual(bits['header'], self.bit1.data.data)
        self.assertEqual(bits['page-block'], self.bit2.data.data)
        self.assertEqual(bits['logo-image'], self.bit3.data.image)

    def tearDown(self):
        """ Cleanup """
        cache.clear()
        shutil.rmtree(settings.MEDIA_ROOT)
