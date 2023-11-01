# -*- coding: utf-8 -*-

# from collective.accordionviews import _
from urllib import request

from bs4 import BeautifulSoup
from plone import api
from plone.app.layout.globals.interfaces import IViewView
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.interface import Interface, alsoProvides


class ITabbedView(Interface):
    """Marker Interface for ITabbedView"""


class TabbedView(BrowserView):
    def __call__(self):
        return self.index()

    @property
    def results(self):
        listing_view = api.content.get_view(
            name="contentlisting", context=self.context, request=self.request
        )
        results = listing_view(exclude_from_nav=False)
        return results

    def tab_is_active(self, item, start):
        tabid = "nav-link-{}".format(item.uuid())
        current_tabid = self.request.get("tabid", None)
        if not current_tabid and start:
            return True
        elif not current_tabid:
            return False
        return current_tabid == tabid

    def render_item(self, item):
        ctx = item.getObject()
        default_page = getattr(ctx.aq_explicit, "default_page", None)
        if default_page:
            ctx = ctx.restrictedTraverse(default_page)
        # without this a leadimage viewlet will not be rendered!
        self.request.set("URL", ctx.absolute_url())
        self.request.set("ACTUAL_URL", ctx.absolute_url())
        view_name = getattr(ctx.aq_explicit, "layout", ctx.getDefaultLayout())
        self.context_view = getMultiAdapter((ctx, self.request), name=view_name)
        alsoProvides(self.context_view, IViewView)
        html_str = self.context_view()
        return self._clean_html(html_str)

    def _clean_html(self, raw_html):
        content_soup = BeautifulSoup(raw_html, "html.parser")
        content = content_soup.select_one("#content-core")
        return content.prettify()
