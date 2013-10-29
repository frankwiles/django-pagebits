django-pagebits
===============

Provide simple like CMS functionality without giving out to much
rope for a user to hang themselves with.

**NOTE**: This is alpha software, I'd suggest not using it yet.

Design
======

Often you want to give users **bits** of editable content around a site, but some of the existing
implemenations such as django-chunks and similar packages are cumbersome to use for one reason or another. You also may want to separate out permissions so that only certain users can define content areas, while others can edit them.

BitGroups
---------

``BitGroup``\s are simply that, a collection of various bits that are logically grouped together on the site. These could be for example:

    * A 'meta-<pagename>' ``BitGroup`` for each page that defines fields for the page title and meta description/keyword tags.
    * A 'homepage-sidebar' ``BitGroup`` that defines various Bits that are displayed there. Perhaps you have header text, two HTML fields, and an image here.
    * A 'homepage-content' ``BitGroup`` that defines 3 Plain Text header bits, 3 HTML bits, and 3 Image bits for a 3 column layout.

``BitGroup``\s optionally lets you show the user two things in the admin interface:

    * A short plain text description of the ``BitGroup``.  For example, "This defines the 3 content areas in the homepage sidebar." which helps the user to more quickly figure where the content is that they want to edit.
    * HTML instructions which will be included in the admin above the editing form. Here you can define whatever more detailed instructions to your end user.

``BitGroup``\s are always referenced by their slug field internally, but can use a more human readable name in the admin interface for the users.

PageBits
--------

Each ``BitGroup`` is made up of one or more ``PageBit``\s. These are entered as an Admin Inline. ``PageBit``\s define what content is allowed:

    1. Plain text which will be escaped on output
    2. HTML which will be automatically marked safe. Using the CKEditor to make things easier.
    3. Image.

They also define the order with which they are to be displayed in the admin interface and whether or not that specific bit is required or not.

The admin interface dynamically constructs a form using the ``PageBit`` order, type, and widget type to construct an easier to understand interface for the user.  Instead of having to hunt around for the 5 different `bits` by name, perhaps prefixing related bits with a common string they have one form to edit per ``BitGroup``.  If we did not group bits together for a typical marketing homepage with had 3 HTML <head> options, 3 on page headers, 3 HTML content areas and 3 images the user would have to click into:

    * homepage_title
    * homepage_meta_description
    * homepage_meta_keywords
    * homepage_header_1
    * homepage_header_2
    * homepage_header_3
    * homepage_content_1
    * homepage_content_2
    * homepage_content_3
    * homepage_image_1
    * homepage_image_2
    * homepage_image_3

From a user's perspective that is a lot of clicking around in the Django Admin just to edit a single "page".  They can't see all of the elements together which can lead to user error.
They may also erroneously assume if they create 'homepage_content_4' that it will magically appear in the template.  Giving them an interface that groups these bits together, defines whether or not a field is required, and what type of data is appropriate for that area solves a lot of these problems.

Using PageBits
==============

You can use PageBits in two ways via templatetags or the ``PageBitView``. Both of these options make it easy to include multiple ``BitGroup``\s in a simple template or view.

tempatetag
----------

An example of how you might use multiple ``BitGroup``\s in a single template using template tags::

    {% extends "base.html" %}
    {% load pagebits %}

    {% block header %}
        {% pagebits 'homepage-meta' as bits %}
        <title>{{ bits.title }}</title>
        <meta name="description" content="{{ bits.description }}" />
        <meta name="keywords" content="{{ bits.keywords }}" />
    {% endblock %}

    {% block content %}
        {% pagebits 'homepage-content' as bits %}

        <img src="{{ bits.image_1 }}" />
        <h1>{{ bits.header_1 }}</h1>
        {{ bits.content_1 }}

        <img src="{{ bits.image_2 }}" />
        <h1>{{ bits.header_2 }}</h1>
        {{ bits.content_2 }}

        <img src="{{ bits.image_3 }}" />
        <h1>{{ bits.header_3 }}</h1>
        {{ bits.content_3 }}
    {% endblock %}

PageBitView
-----------

You can also use PageBits as a slightly smart ``TemplateView``. This would define a simple URL, using a specified template with the same two ``BitGroup``\s as above in a ``urls.py``::

    from django.conf.urls import patterns, url
    from pagebits.views import PageBitView

    urlpatters = patterns('',
        url(
            regex=r'^homage.html$',
            view=PageBitView.as_view(),
            name='homepage',
            kwargs={
                'template_name': 'home.html',
                'group_slugs': ['homepage-meta', 'homepage-content'],
            },
        )
    )

PageBit views incorporate the ``PageBit`` context names in order of definition.  This allows you to do override content areas with a fall back pattern.  For example you could set it up like::

    'group_slugs': [
        'default-meta',
        'homepage-meta',
        'default-sidebar',
        'homepage-sidebar',
        'homepage-content'
    ]

Assuming the 'homepage-meta' and 'homepage-sidebar' ``BitGroup``\s had all optional fields, this would allow you to give the user the ability to show some default content on pages, but also override specific pages with page specific content where needed.

Fallback Pages
--------------

These work much like Django's stock flatpage contrib application.  You define ``PageTemplate``\s that are available to users.  You can then define ``Page``\s that associate a URL, a ``PageTemplate``, and one or more ``BitGroup``\s to display in that page.

This can be done by either including the urls.py as a "catch all" like so::

    from pagebits.views import PageView

    # Your normal URL patterns here, it is important to put the
    # catchall at the end

    urlpatterns += patterns('',
        (r'^(?P<url>.*)$', PageView.as_view()),
    )

Caching
=======

This sort of model structure, without caching, performs very poorly.  Many ORM lookups happen to make this easy to use and decently structured.  ``django-pagebits`` automatically caches these values for you.

Settings
========

Settings that control caching and their defaults::

    PAGEBIT_CACHE_PREFIX = 'pagebits'
    PAGEBIT_CACHE_TIMEOUT = 3600

Running Tests
=============

Setup (you must have Postgres installed & setup)::

    $ createdb pagebits
    $ git clone https://github.com/frankwiles/django-pagebits.git
    $ cd django-pagebits
    $ virtualenv env
    $ . env/bin/activate
    $ python setup.py develop
    $ pip install -r pagebits/tests/requirements.txt

Running the tests:

    $ . env/bin/activate
    $ cd pagebits
    $ django-admin.py test pagebits --settings=pagebits.tests.settings
