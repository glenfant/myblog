A simple benchmark getting the site object
##########################################
:date: 2008-05-10 10:57
:author: Gilles Lenfant
:tags: Plone, Zope 2, Zope 3
:category: Blog
:slug: a-simple-benchmark-getting-the-site-object
:status: published
:summary: Different ways to get the Plone site object

Hi,

Ho many of you complain about Plone performances? The latest Plone
release are said to be faster than the former ones.

Her is a sample benchmark that compares the three ways to get the portal
(Plone) object.

-  The first one, I found it when wandering in the Zope 3 subset that
   ships with Zope 2.10.
-  The second one is the recommanded practice since Plone 3, getting the
   ``plone_portal_state`` multi adapter.
-  And the third one is the (somehow deprecated?) CMF style to get the
   portal object.

Here is the code as external method, just copy it in an appropriate
place, and add the external method where you want in your Plone site.

.. code-block:: python

    from zope.app.component.hooks import getSite
    from zope.component import getMultiAdapter
    from Products.CMFCore.utils import getToolByName
    from time import time as time_now
    from StringIO import StringIO

    COUNT = 1000

    def testGetPlone(self):
        """Small benchmark"""

        out = StringIO()
        request = self.REQUEST
        t0 = time_now()

        for x in xrange(COUNT):
            plone = getSite()
        t1 = time_now()

        for x in xrange(COUNT):
            plone = getMultiAdapter(
                (self, request),
                name="plone_portal_state").portal()
        t2 = time_now()

        for x in xrange(COUNT):
            plone = getToolByName(self, 'portal_url').getPortalObject()
        t3 = time_now()

        print >> out, COUNT, "times getSite Zope 3 function:", t1 - t0, "seconds"
        print >> out, COUNT, "times plone_portal_state multi adapter:", t2 - t1, "seconds"
        print >> out, COUNT, "times old style getToolByName:", t3 - t2, "seconds"
        return out.getvalue()

Yeah and here are the results on my MacBook:

.. code-block:: console

    1000 times getSite Zope 3 function: 0.000494956970215 seconds
    1000 times plone_portal_state multi adapter: 0.0551428794861 seconds
    1000 times old style getToolByName: 0.0382490158081 seconds

What conclusions can we expose here?

#. The old style and deprecated ``getToolByName`` is **faster** than the
   new style way that uses the ``plone_portal_state`` multi adapter that
   is supposed to cache the result! I ran the test several times to
   confirm this is not a bad trip or beer abuse effect. No, this is
   true, just continue using the old CMF style way to get a tool or the
   portal.
#. The (poorly used in Plone) Zope 3 "getSite" does not need a context
   or request object to get the site object. Wow! Interresting in lots
   of design situations. And in addition, it is **100 times** faster
   than the "official" APIs.
#. Zope 3 offers new services that deserve to be used more and more.
   Plone suffers of serious performances issues, more particularly for
   authenticated users, sorry to say this but it's true. We shouldn't
   need to use ZEO or Squid when 10 authenticated users manage content
   in a Plone site.

Okay, that benchmark does not match real applications. Who searches 1000
times the portal object in a Plone based app?

But there are certainly dozen of other tricky things in Plone,
Archetypes or CMF that should be re designed to address the Plone
performance issues.

Have you guys found other hints to have a faster Plone without the need
to cache somewhere?
