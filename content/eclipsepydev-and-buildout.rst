Eclipse/pydev and buildout
##########################
:date: 2008-05-25 15:51
:author: Gilles Lenfant
:tags: Plone
:category: Blog
:slug: eclipsepydev-and-buildout
:status: published
:summary: An Eclipse / Pydev helper to enable smart completion on a zc.buildout project.

`Pydev <http://pydev.sourceforge.net/>`__ has a nice code completion feature
when editing Python code. You start typing a name, and Eclipse/Pydev offers
context specific completions with call tips that saves a lot of time when
programming for a hugh framework like Plone.

This requires to stuff somehow the PYTHONPATH for your project. This is fairly
easy with a Plone bundle install tarball, where you just need to provide the
paths to the Products directory, the ``lib/python`` of your instance and the
global Zope ``$SOFTWARE_HOME``.

With an instance created with buildout, things are not as
straightforward. Such an instance is made of tons of eggs that are not
in the standard "site-packages", in addition, Zope 2 style products may
be located in various places. Adding all this manually in the Pydev
project PYTHONPATH is a real nightmare.

Hopefully we have two recipe companions who can help us a lot
configuring Eclipse + Pydev on your buildout instance:

- `iw.recipe.cmd <http://pypi.python.org/pypi/iw.recipe.cmd>`__ that
  builds some symlinks tree, with the help of some Python lines, for...

- `pb.recipe.pydev <http://pypi.python.org/pypi/pb.recipes.pydev/>`__
  that makes most of the job

From now we assume you already have a ready Plone 3.x instance.

With Eclipse, create a new Pydev project, say at the root of your
buildout. Do not add anything to the Pydev - PYTHONPATH of that project.
Now quit Eclipse. Your instance root should have a ``.pydevproject`` file.

Open your ``buildout.cfg`` and add that stuff:

.. code-block:: ini

   [buildout]
   ...
   zope-directory = /path/to/your/Zope-2.10.5
   ...
   parts =
       ...
       make_pydev_init_files
       pydev
       ...
   # Do not add parts that add eggs or products after the above parts
   ...
   [make_pydev_init_files]
   # we need this (a Products directory with symlinks to all plone products)
   # to have completion of code in the Products namespace
   recipe = iw.recipe.cmd:py
   on_install = true
   cmds =
         >>> import os
         >>> dirs = """${instance:products}""".split("\n")
         >>> prodlinks = os.path.join("""${buildout:directory}""".strip() , 'pydevlinks')
         >>> Products = os.path.join(prodlinks,'Products')
         >>> if not os.path.isdir(prodlinks): os.mkdir(prodlinks)
         >>> if not os.path.isdir(Products): os.mkdir(Products)
         >>> file(os.path.join(Products , '__init__.py'),'w').write('#')
         >>> for dir in dirs:
         >>>     if not dir: continue
         >>>     for product in [os.path.join(dir,a) for a in os.listdir(dir) if os.path.isdir(os.path.join(dir,))]:
         >>>         linkname = os.path.join(Products, os.path.basename(product))
         >>>         if not os.path.islink(linkname): os.symlink(product,linkname)

   [pydev]
   recipe = pb.recipes.pydev
   eggs = ${instance:eggs}

   # See [make_pydev_init_files] below
   extra_paths =
       ${buildout:directory}/pydevlinks
       ${buildout:zope-directory}/lib/python
   pydevproject_path = ${buildout:directory}/.pydevproject

Re-run your buildout. That's OK? Now open Eclipse and view your project
properties. Et voilà...

.. figure:: {filename}/images/pydev-pythonpath.png
   :alt: Eclipse dashboard

   PYTHONPATH of Eclipse / Pydev environment

As you can see we use "os.symlink" to fake a products hierarchy. Windows
(NTFS) users should install a symlink tool like
"`junction <http://www.microsoft.com/technet/sysinternals/fileanddisk/junction.mspx>`__"
and tweak the script of the ``make_pydev_init_files`` part.

.. admonition:: Caveat

   do not change manually anything that's in the ``/prodlinks`` directory of
   your buildout unless...

Many thanks to `Tim Knapp and
Sylvio <http://www.nabble.com/-Fwd%3A-Re%3A--Product-Developers--buildout-and-eclipse--td16697376s20094.html#a16699863>`__
for the hints in the products developers mailing list. Now this is in a
blog.
