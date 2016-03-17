Safer GenericSetup upgrade steps
################################
:date: 2008-09-18 16:27
:author: Gilles Lenfant
:tags: Plone
:category: Blog
:slug: safer-genericsetup-upgrade-steps
:status: published
:summary: Protect upgrade steps from being ran in bad places.

Upgrading Plone extensions using GenericSetup upgrade steps. A great idea.
Easy to develop, easy to use and document. A unified upgrade interface for
every Plone extension.

Anyway, there's actually an annoying issue on upgrade steps: upgrade steps for
component "foo" are exposed in sites where the "foo" component is **not
installed**.

Wow, managers on instances where various different Plone sites are installed
have to be careful on this. Running an upgrade step of a component that is not
installed in a site may be harmful. Even if upgrade scripts are supposed to be
defensively programmed.

Having several Plone extensions, I made a decorator based generic safety belt.
Of course this does not prevent GS showing the upgrade steps but executing
such upgrade steps raises an explicit error message and does not execute the
upgrade step.

Just add these lines to your ``utils.py``:

.. code-block:: python

   from zope.component import getUtility
   from Products.CMFCore.interfaces import ISiteRoot
   from config import PROJECTNAME

   class NotInstalledComponent(LookupError):
       def __init__(self, cpt_name):
           self.cpt_name = cpt_name
           return

       def __str__(self):
           msg = ("Component '%s' is not installed in this site."
                  " You can't run its upgrade steps."
                   % self.cpt_name)
           return msg

   class IfInstalled(object):
       """The decorator"""
       def __init__(self, prod_name=PROJECTNAME):
           """@param prod_name: as shown in quick installer"""
           self.prod_name = prod_name

       def __call__(self, func):
           """@param func: the decorated function"""
           def wrapper(setuptool):
               portal = getUtility(ISiteRoot)
               qi = portal.portal_quickinstaller
               installed_ids = [p['id'] for p in qi.listInstalledProducts()]
               if self.prod_name not in installed_ids:
                   raise NotInstalledComponent(self.prod_name)
               return func(setuptool)
           wrapper.__name__ = func.__name__
           wrapper.__dict__.update(func.__dict__)
           wrapper.__doc__ = func.__doc__
           wrapper.__module__ = func.__module__
           return wrapper

Then your upgrade scripts should be decorated like this in your ``upgrades.py``.

.. code-block:: python

    from utils import IfInstalled
    @IfInstalled()
    def someUpgradeFunction(setuptool):
        # Stuff as usual...

You're done...
