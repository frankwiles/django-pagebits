import os
import shutil

from django.core.files import File
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase

from ..models import BitGroup, PageBit, PageTemplate, Page


class PageBitViewTests(TestCase):

    def setUp(self):
        self.group = BitGroup.objects.create(name='testgroup')
        self.bit1 = PageBit.objects.create(
            name='header',
            context_name='header',
            type=0,
            group=self.group
        )
        self.bit1.data.data = 'Test Page Header'
        self.bit1.data.save()

        self.bit2 = PageBit.objects.create(
            name='page block',
            context_name='page_block',
            type=1,
            group=self.group
        )

        self.bit2.data.data = '<p>Block</p>'
        self.bit2.data.save()

        self.bit3 = PageBit.objects.create(
            name='logo image',
            context_name='logo_image',
            type=2,
            group=self.group
        )
        f = open(os.path.join(os.path.dirname(__file__), 'test-image.jpg'))
        myfile = File(f)

        self.bit3.data.image = myfile
        self.bit3.data.save()

    def test_view(self):
        response = self.client.get(reverse('testview'))
        self.assertEqual(response.context['header'], self.bit1.data.data)
        self.assertEqual(response.context['page_block'], self.bit2.data.data)
        self.assertEqual(response.context['logo_image'], self.bit3.data.image)

    def test_fallback_pages(self):
        template = PageTemplate.objects.create(name='test', path='test.html')
        page = Page.objects.create(
            name='Test',
            url='test2/test/',
            template=template,
        )
        page.bit_groups.add(self.group)

        response = self.client.get('/test2/test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['header'], self.bit1.data.data)
        self.assertEqual(response.context['page_block'], self.bit2.data.data)

        response = self.client.get('/notest/nohere/')
        self.assertEqual(response.status_code, 404)

    def test_middlware_pages(self):
        template = PageTemplate.objects.create(name='test', path='test.html')
        page = Page.objects.create(
            name='Test',
            url='test3/test/',
            template=template,
        )
        page.bit_groups.add(self.group)

        response = self.client.get('/test3/test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['header'], self.bit1.data.data)
        self.assertEqual(response.context['page_block'], self.bit2.data.data)

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)
