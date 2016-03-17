Step debugging a Zope 2 / Plone instance with Eclipse + PyDev
#############################################################
:date: 2011-11-07 01:02
:author: Gilles Lenfant
:tags: Plone, Zope 2
:category: Blog
:slug: step-debugging-zope-eclipse-pydev
:status: published
:summary: Step debug and objects inspection of a live Plone site with Eclipse / Pydev

Hi,

Most power users mays already know this. But this is a real
enlightenment for newbies who are stuck with the command line pdb
utility. Even for experienced developper as I am... supposed to be, this
is a real advantage to have on screen at the same time the source code,
with breakpoints in the margin of it, the inspector for your global and
local variables, the access to the call stack and execution frames.

Start reading `the fine manual
here <http://www.pydev.org/manual_adv_remote_debugger.html>`__ and come
back reading how to get this in Zope 2.

Of course I assume you have a recent Eclipse (Indigo) and Pydev (2.2.4)

Find in your Eclipse software directory the full path of the directory
that contains ``pydevd.py``. In other words :

.. code-block:: console

   $ cd /your/eclipse/root
   $ find . -name 'pydevd.py'

In my MacBook the file is found in
``/Developer/eclipse/plugins/org.python.pydev.debug\_2.2.4.2011110216/pysrc``

(note that upgrades of PyDev may change this path to something else)

Edit your development buildout config file and add this in your
plone.recipe.zope2instance part:

.. code-block:: ini

   [instance]
   # recipe = plone.recipe.zope2instance
   ...
   extra-paths =
       /Developer/eclipse/plugins/org.python.pydev.debug_2.2.4.2011110216/pysrc

Of course re-run your buildout. Open the debug perspective in Eclipse
and start the PyDev debugger server (see link above).

You can now add anywhere you want (need) the line:

.. code-block:: python

   import pydevd;pydevd.set_trace()

or create and useuse the shortcut "pydevd" to insert your first hard breakpoint.

Start your Zope instance and make the necessary clicks to execute the line
that has the hard breakpoint. Wow, great : the next line of Python to be
executed is hilited from there, you cand step, step over, go to the next
return, and even add soft breakpoint double clicking in the left margin
anywhere in your source code.

All other things you may need to know about debugging with PyDev `are here
<http://www.pydev.org/manual_adv_debugger.html>`__ and usable "as is" in a
Zope server.

Another great feature for those who develop with Windows: when debugging with
Eclipse/Pydev you can start your development instance as a service, when
before you needed to run the sloooooow "instance fg" and benefit of Eclipse
remote debugging.
