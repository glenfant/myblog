ZCML Wadda ? Want a live ZCML doc ?
###################################
:date: 2011-04-20 16:54
:author: Gilles Lenfant
:tags: Frameworks, Zope 2
:category: Blog
:slug: zcml-wadda-want-a-live-zcml-doc
:status: published
:summary: How to get the ZCML doc that fits your zope instance

Abstract
========

ZCML is a great feature in Zope 2 since the first Five years. Exploring
a well designed Python package starts with its ZCML files and its main
"interfaces.py" module.

But newbies as I have been and others have pain to remember the various
ZCML directives available, as well as the detailed attributes of them.

Of course there are some documentations in printed books or in various
blogs or docs about most directives. But there's no central point
(unless I didn't search correctly) where you can read the documentation
for all ZCML directives available in **your** Zope 2 instance with third
party components that could add new ZCML vocabulary.

Of course, you may grep all "meta.zcml" files in your instance, search
for the appropriate namespace, then the appropriate directive. And
finally open the Python file that defines the schema of the mysterious
ZCML, just as I explained in `another ZCML related blog
post <http://glenfant.wordpress.com/2008/05/09/doing-my-zcml/>`__.

Grepping the "zope.configuration", I hopefully found a magic function
that provides a structured tree of all the registered ZCML directives
well suited to provide a live documentation.

After some hours of work and exploration, I'm proud to give to the Zope
2 community
"`aws.zope2zcmldoc <http://pypi.python.org/pypi/aws.zope2zcmldoc>`__"
that provides a live documentation on all ZCML namespaces, directives
and subdirectives installed in your Zope 2 instance.

Some screenshots
================

|Available from the standard Zope control panel|

|All namespaces|

|The "browser" namespace|

|The "pages" directive|

You can notice that the description text are translated in your favorite
language when the translation is available.

``aws.zope2zcmldoc`` is the new companion of ``Products.DocFinderTab``,
``plone.reload``, ``Products.Clouseau`` and ``zope2.zodbbrowser`` (and perhaps
others I forgot, sorry) to your development instances.

Any feedback, is welcome.  Enjoy !

Ah yes, and many thanks to my actual employer `Alter
Way <http://www.alterway.fr>`__ for sponsoring this piece of software.

.. |Available from the standard Zope control panel| image:: http://glenfant.files.wordpress.com/2011/04/control-panel.png
   :target: http://glenfant.files.wordpress.com/2011/04/control-panel.png
.. |All namespaces| image:: http://glenfant.files.wordpress.com/2011/04/namespaces.png
   :target: http://glenfant.files.wordpress.com/2011/04/namespaces.png
.. |The "browser" namespace| image:: http://glenfant.files.wordpress.com/2011/04/browser-namespace.png
   :target: http://glenfant.files.wordpress.com/2011/04/browser-namespace.png
.. |The "pages" directive| image:: http://glenfant.files.wordpress.com/2011/04/browser-pages.png
   :target: http://glenfant.files.wordpress.com/2011/04/browser-pages.png
