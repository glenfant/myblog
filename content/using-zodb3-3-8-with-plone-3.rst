Using ZODB3 3.8 with Plone 3
############################
:date: 2010-12-18 16:08
:author: Gilles Lenfant
:tags: Plone, Zope 2
:category: Blog
:slug: using-zodb3-3-8-with-plone-3
:status: published
:summary: Use a safer ZODB back-end if you're stuck with Plone 3

Background
==========

Lots of you are still in process of maintaining Plone 3 sites for yourself or
customers and didn't go to Plone 4 for some good reason.

The Plone 3 bundle is powered and tested with the latest Zope 2.10. This Zope
version itself includes ZODB3 3.7. That has lots of issues that are now gone
with later versions.

But wait, it's not possible to use ZODB3 3.10.x since it seems it requires
Python 2.6. ZODB3 3.9.x too has too many API changes and it seems that we need
to go to a full Zope 2.11 to support this lates version.

ZODB3 3.8 seems a reasonable choice to improve the persistence support of your
Plone 3 apps.

-  It compiles with Python 2.4- It has a lot of new features
-  It has a lot of bugfixes
-  It has lots of additional tests, thus should be more reliable

Have a look at
http://pypi.python.org/pypi/ZODB3/3.8.6#whats-new-in-zodb-3-8-6-2010-09-21
to see all the details.

This sample buildout extends the standard "buildout.cfg" that comes with the
ZopeSket template "plone3\_buildout", and replaces the ZODB3 that comes with
Zope 2.1.0 by the ZODB3 3.8.6 egg, as well as some Zope 2 components that need
an explicit upgrade to cope with this new ZODB3 version.

--------------

.. code-block:: ini

   [buildout]
   # buildout.cfg as built from plone3_buildout ZopeSkel template
   extends = buildout.cfg
   eggs +=
       zope.proxy
       ZODB3
       zodbcode
       tempstorage

   [zope2]
   skip-fake-eggs =
       ZODB3
       zope.proxy
       zodbcode
       tempstorage
   [versions]
   # Marked as additional fake egg in [zope2]
   ZODB3 = 3.8.6
   zope.proxy = 3.4
   zodbcode = 3.4.0
   tempstorage = 2.11.3

--------------

Some warnings and gotchas
=========================

-  This configuration has been tested as simple instance deployment. I
   didn't yet test a ZEO cluster in such situation.
-  This configuration has been tested successfully with only some well
   known third party extension : LinguaPlone, Collage, PloneFormgen,
   Ploneboard. Some third party Plone extensions that may play with ZODB
   inners should be tested in depth (run at least unit tests) before
   going in production.


Other things
------------

If something is going wrong with this new ZODB, you can go back to the
original ZODB3 that comes with Zope 2.10.x. Unless you have been playing with
new storages and options that come with ZODB3 3.8.

Any feedback of others who tried this recipe or similar ones is welcome.
