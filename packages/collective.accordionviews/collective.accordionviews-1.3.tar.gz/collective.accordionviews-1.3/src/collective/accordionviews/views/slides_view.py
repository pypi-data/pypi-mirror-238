# -*- coding: utf-8 -*-

# from collective.accordionviews import _
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ISlidesView(Interface):
    """Marker Interface for ISlidesView"""


class SlidesView(BrowserView):
    def __call__(self):
        return self.index()

    @property
    def results(self):
        listing_view = api.content.get_view(
            name="contentlisting", context=self.context, request=self.request
        )
        results = listing_view(portal_type="Image")
        return results
