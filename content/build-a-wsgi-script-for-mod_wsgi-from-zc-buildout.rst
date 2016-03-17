Build a WSGI script for mod_wsgi from zc.buildout
#################################################
:date: 2013-06-29 14:46
:author: Gilles Lenfant
:tags: Buildout, Python
:category: Blog
:slug: build-a-wsgi-script-for-mod_wsgi-from-zc-buildout
:status: published
:summary: How to create automatically a WSGI script from a zc.buildout config with correct sys.path setup.

Forewords
=========

While building a `Flask <http://flask.pocoo.org/>`__ application with
`zc.buildout <https://pypi.python.org/pypi/zc.buildout/>`__, I have been
searching a way to build the script for Apache's `mod_wsgi
<https://code.google.com/p/modwsgi/>`__ directly from the buildout command.

Being brain dumb, having other emergencies, and being a lazy programmer, I
asked to `stackoverflow for some hints
<http://stackoverflow.com/questions/12836832/building-the-wsgi-script-for-flask-with-zc-buildout>`__.

My fellow `Gaël Pasgrimaud <http://www.gawel.org/>`__ suggests using
`collective.recipe.modwsgi <https://pypi.python.org/pypi/collective.recipe.modwsgi/>`__
but I did not want to add the `PasteDeploy monster <http://pythonpaste.org/deploy/>`__
to my software stack.

So I took time to hack `zc.recipe.egg
<https://pypi.python.org/pypi/zc.recipe.egg/2.0.0>`__ and find how it creates
custom scripts. Et voilà...

I found a way to create my custom **wsgi script** just using the great
`z3c.recipe.runscript <https://pypi.python.org/pypi/z3c.recipe.runscript>`__,
I already use for other purposes in various projects.
``z3c.recipe.runscript`` is a great piece of software that helps
creating your own custom small recipes when you don't find what you need
in Pypi or have time to create a real zc.buildout recipe. Here are the
snips you need to do the same in your project :

A snip of buildout.cfg
======================

[gist:id=5890957]

.. [gist https://gist.github.com/glenfant/5890957 /]

The three parameters expected from this custom part are :

**egg**

The egg name that contains the wsgi app code.

**script**

The full path to the wsgi script that will  be generated, the same path
should sit to the right of
the `WSGIScriptAlias <https://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIScriptAlias>`__ in
your Apache config.

**app**

The Python name of the application object in the above mentioned egg.

And the snip of above referenced **buildouthelpers.py**:

[gist:id=5890964]

Some assumptions without which none of this works:

-  Your wsgi app sits in the **egg.with.wsgiapp** egg.
-  This **egg.with.wsgiapp** egg is installed in another buildout part
   using **zc.recipe.egg** recipe (or another one that relies on it),
   and this part is executed **before [wsgiscript]**.
-  All requirements for **egg.with.wsgiapp** must sit in its **setup()**
   parameter **install_requires** and not in a pip requirements file.

Hope this will help others who fell in a similar situation. Any question
or improvement suggestion is welcome.
