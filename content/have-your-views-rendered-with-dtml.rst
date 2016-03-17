Have your views rendered with DTML
##################################
:date: 2008-08-16 19:23
:author: Gilles Lenfant
:tags: Plone
:category: Blog
:slug: have-your-views-rendered-with-dtml
:status: published
:summary: DTML can still be used easily in Plone views.

Have your views rendered with DTML
==================================

As we're supposed to kill the CMF skins layer in the Plone components, when
tailoring the old style products to components, we put all static data
(images, javascripts, stylesheets) in resources directories, python scripts to
views and adpters, controller page templates to plone.app.form or
plone.app.z3cform schemes, and so on...

But the new style resource directory doesn't take care about DTML as it does
for page templates. And for some kinds of stuffs like dynamic CSS/Javascript,
or making a CSV file, DTML is yet the better suited than ZPT.

Yes you can publish DTML based views/pages/viewlets. This is not obvious but
not that much complicated. This small example shows how to add a stylesheet
using the standard Plone ``base_properties`` CSS data.

First the ZCML bunch at .../browser/configure.zcml:

.. code-block:: xml

   <browser:page
     name="mystytles.css"
     for="Products.CMFPlone.interfaces.IPloneSiteRoot"
     class=".stylesheet.MyStylesheet"
     permission="zope2.Public"
   />

So we'll have that sthylesheet published at http://<your-site>/mystyles.css.

Now the .../browser/stylesheet.py module:

.. code-block:: python

   ...
   import os
   from Globals import DTMLFile

   from Products.Five.browser import BrowserView
   ...
   this_dir = os.path.dirname(os.path.abspath(__file__))

   templates_dir = os.path.join(this_dir, 'templates')
   # Don't add ".dtml" to the file name though the file is "mystyles.css.dtml"
   mystylesheet_dtml = DTMLFile('mystyles.css', templates_dir)

   ...
   class MyStylesheet(BrowserView):
       def __call__(self, *args, **kw):
           """This view is published"""

           # Wrap acquisition context to template
           template = mystylesheet_dtml.__of__(self.context)

           # Note that you can provide other named args below you might need in
           # your template
           return template(context=context)

And finally our DTML template at .../browser/templates/mystyles.css.dtml

.. code-block:: text

   /* <dtml-with "context.base_properties"> (do not remove this :)
   <dtml-let portal_url="context.absolute_url()"> (do not remove this :)
   */

   .silly {
     color: &dtml-discreetColor;;
   }
   .foo {
     background: &dtml-portal_url;/some-image.gif;
   }

   /* </dtml-let></dtml-with> (do not remove this :) */

You just need to add "mystyles.css" to the Plone CSS registry but that's
another story. That's all folks.

Note that you could prefer using
`z3c.zrtresource <http://pypi.python.org/pypi/z3c.zrtresource>`__ if
you're bleeding-edge oriented developer.
