Using decorated functions in ZCML
#################################
:date: 2008-06-09 11:05
:author: Gilles Lenfant
:tags: Plone, Zope 2, Zope 3
:category: Blog
:slug: using-decorated-functions-in-zcml
:status: published
:summary: Decorators play with object external names. Don't let it do.

As python programmer, I love the elegant way to tweak function behaviours with
decorators.

In order not to be executed when another profile is invoked, most setup
handler functions must start with:

.. code-block:: python

   def setupSomeStuff(context):
       if context.readDataFile("mysite.txt") is None:
           return
       # Let's do the job baby
       ...
       return

As the site I'm working on needs a lot of handlers that are used in various
conditions like this one. But there are lots of such...

.. code-block:: xml

   <gs:importStep
      name="Products.MySite.setupSomeStuff"
      title="Stuff that site"
      description="D'ya know what stuffing means..."
      handler="Products.MySite.setuphandlers.setupSomeStuff">
      <depends name="Products.MySite.importSiteStructure" />
   </gs:importStep>

...and of course as many setup handler functions.

In order to shorten a little bit the code, I made a simple decorator that
executes the setup handler only in the context of the extension profile.
Should be fine.

.. code-block:: python

   def thisProfileOnly(func):
       """Decorator that prevents the setup func to be used on other GS profiles.
       Usage:
       @thisProfileOnly
       def someFunc(context): ...
       """

       def wrapper(context):
           if context.readDataFile('mysite.txt') is None:
               logger.info("*NOT* Executing setuphandler function %s", func.__name__)
               return
           else:
               logger.info("Executing setuphandler function %s", func.__name__)
               return func(context)

   @thisProfileOnly
   def setupSomeStuff(context):
       # Let's do the job baby
       ...
       return

Let's go baby... But wait... It does not work! Importing the profile doe
not run the setup handlers.

Having a deeper look into all this, I found that the relevant
GenericSetup registry does hold the decorated functions but the unbound
wrapper itself. Bad news.

Is it a bug or a feature? Anyway, digging in the Python gurus blogs, I
found how to work this around, augmenting the wrapper such it gets most
of the decorated function signature. Follow the lines in red in the
fixed decorator.

.. code-block:: python

   def thisProfileOnly(func):
       """Decorator that prevents the setup func to be used on other GS profiles.
       Usage:
       @thisProfileOnly
       def someFunc(context): ...
       """

       def wrapper(context):
           if context.readDataFile('modulo.txt') is None:
               logger.info("*NOT* Executing setuphandler function %s", func.__name__)
               return
           else:
               logger.info("Executing setuphandler function %s", func.__name__)
               return func(context)
       wrapper.__name__ = func.__name__
       wrapper.__dict__.update(func.__dict__)
       wrapper.__doc__ = func.__doc__
       wrapper.__module__ = func.__module__
       return wrapper

Yes, with such decorators, you may use decorated functions in your ZCML.

Note that this should be useless from Python 2.5, but I didn't test in
such situation (too lazy to try to run the Zope/Plone machinery with
Python 2.5).

.. admonition:: Note

   As of Python 2.5, you do't need this antmore. Rather use the
   ``functools.wraps`` decorator to have the same effect.

Other sources about advanced Python decorators:

-  `Charming Python: decorators make magic
   easy <http://www.ibm.com/developerworks/linux/library/l-cpdecor.html>`__
-  `The decorator
   module <http://www.phyast.pitt.edu/~micheles/python/documentation.html>`__
