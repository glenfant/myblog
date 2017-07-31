From dotted name to object
##########################
:date: 2017-07-31 13:01
:author: Gilles Lenfant
:category: Blog
:tags: Python; Tip
:slug: from-str-to-obj
:status: published
:summary: Make an object drom a simple dotted name

It is sometimes useful to be in position to select an arbitrary Python global object from a config file or some command line option. Things like this are called "dotted names".

That helper is a small undocumented treasure hidden in the stdlib ``pydoc`` module called
``locate``.

.. code-block:: pycon

   >>> import pydoc
   >>> MY_PI = pydoc.locate('math.pi')
   >>> import math
   >>> MY_PI
   3.141592653589793
   >>> MY_PI is math.pi
   True

Enjoy...
