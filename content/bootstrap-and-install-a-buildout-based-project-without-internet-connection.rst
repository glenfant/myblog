Bootstrap and install a buildout based project without Internet connection
##########################################################################
:date: 2011-07-31 20:30
:author: Gilles Lenfant
:tags: Buildout
:category: Blog
:slug: bootstrap-and-install-a-buildout-based-project-without-internet-connection
:status: published
:summary: How can you deploy a zc.buildout project without an Internet connection on the target host.

Background
----------

Complex Python based solutions are now built with the great
**zc.buildout**, like complicated ZEO clusters with heavily customized
Plone site or others.

zc.buildout is a great solution that's now essential to share among developers
a custom project as well as for distributing to users or customers. As
everybody know, zc.buildout grabs components from the Internet (mostly from
the Pypi site) and makes the application assembling those components according
to the integration directives in the various ``*.cfg`` files. But talking
about zc.buildout in details in not the purpose of this blog post of course.

Installing the solution in the customer's computers is supposed to be
easy and straightforward. "Unfortunately", running zc.buildout requires
to bootstrap the project with the famous
"`bootstrap.py <http://svn.zope.org/repos/main/zc.buildout/trunk/bootstrap/bootstrap.py>`__"
file.

This script downloads and installs some essential resources that enable to run
the "bin/buildout" command, like `distribute
<http://pypi.python.org/pypi/distribute>`__ and `zc.buildout
<http://pypi.python.org/pypi/zc.buildout>`__ itself. But with some customers,
there is no possible Internet connection on the installation target, due to a
strict security policy. And I don't want to write a complicated installation
manual that works around this issue. In addition, these customer have little
or no IT required skills.

After asking to some experts in the Plone mailing lists, some answers provided
some pointers from which I made my "`offline\_bootstrap.py
<http://plone.fr/Members/glenfant/offline_bootstrap.py/view>`__" script that
must be used in place of the classical "bootstrap.py" script in such
situations.

The solution
------------

Prepare your buildout structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In particular, you must ensure that your "buildout.cfg" file has these
options:

.. code-block:: ini

   [buildout]
   ...
   # All packages are downloaded locally.
   download-cache = downloads
   # All eggs are installed here
   eggs-directory = eggs
   # You need this if there is an "extends = http://..."
   extends-cache = ext-cache
   ...
   versions = versions
   ...
   [versions]
   ...
   # Freeze your zc.buildout preferred version!
   zc.buildout = x.y.z

Add to the buildout directory the `"offline_bootstrap.py" script you
can grab
here <http://plone.fr/Members/glenfant/offline_bootstrap.py/view>`__.

From the same place add a "**bootstrap_resources/**" directory. In
this directory, add:

-  "`distribute_setup.py <http://python-distribute.org/distribute_setup.py>`__"

-  "**distribute-x.y.z.tar.gz**". *Important*: Use the same version as the one
   indicated by the **DEFAULT_VERSION** in above mentioned
   "**distribute_setup.py**". `Find it from here
   <http://pypi.python.org/pypi/distribute>`__.

- "**zc.buildout-x.y.z.tar.gz**". *Important*: Use exactly the same version as
  the one pinned in your "**buildout.cfg**" as above described. `Find it from
  here <http://pypi.python.org/pypi/zc.buildout>`__

From now you can bootstrap your zc.buildout and carry on developing / testing
/ documenting your Python project as usual.

Installing in an no-Internet platform
-------------------------------------

Your beautiful project is ready to be installed in a customer computer that
has no connection to the Internet. First add a new file in your buildout:
"**production_install.cfg**" with these few lines:

.. code-block:: ini

   [buildout]
   extends = production.cfg
   install-from-cache = true
   offline = true
   newest = false

Of course, I assume you made a "**production.cfg**" buildout profile that
smiles on your integration platform.

You may now remove the database (typically the "**var/**" folder) from the
buildout directory and make a tarball.

Inflate this tarball in the place your customer wants it on his computer. From
the newly created folder, you just need to say this to the console:

.. code-block:: console

   $ python offline_bootstrap.py -c production_install.cfg
   $ bin/buildout -c production_install.cfg

That should be all unless other application specific operations.

Other things about "offline_bootstrap.py"
-----------------------------------------

"**offline_bootstrap.py**" accepts any option and argument the usual
"**bootstrap.py**" takes. Except ``--setup-source`` and ``--download-base`` that
**are set specifically by offline_bootstrap.py**.

Questions or comments ?
-----------------------

... are welcome.
