Doing my ZCML
#############
:date: 2008-05-09 12:46
:author: Gilles Lenfant
:tags: Plone, Zope 2, Zope 3
:category: Blog
:slug: doing-my-zcml
:status: published
:summary: Make your custom ZCML directives

Forewords
=========

Howdy folks,

Lots of us, poor Plone components developers, have been somehow stuck
discovering the new Plone 3 architecture before having some
enlightenments from plone.org documentation or various blogs or better,
from Martin Aspeli essential book.

Across most new programming behaviours, you noticed the massive use of
ZCML coming along with the various components, packages or products [*]_
that ship with Plone 3 bundle.

At first glance, I had some pain trying to understand what's behind the
scene and as Zope 3 dummy, didn't understand why we should use such a
cryptic damned notation. Okay, why should we learn another language when
we can do all this in Python? I heard ZCML is for site integrators.
Well, for those integrators who already know how to read Python source
but certainly not the ones who expand products then play in ZMI to add
features in a Plone site.

In addition, finding good tutorials on ZCML usage in Plone 3 was painful
before fall 2007.

So far, so good, I started to upgrade some public Plone extension
products using ZCML without really understanding fully the "how what
why" of all this, and it worked. But why?

Among the products I'm prettily proud to maintain, there's
`FileSystemStorage <http://plone.org/products/filesystemstorage>`__
(FSS) that's now "componentized" the Plone 3 way to ease its
installation with buildout (but that's another story). For those who
didn't click here, FSS let your Archetypes content types store fieds
values directly in the file system rather than in plain ZODB object
attributes or annotations. This saves memory in Plone sites that serve
lots of big files.

Code or configuration
=====================

Bind with code
--------------

There's two ways to use FSS from content types.

(a) Using FSS in your own content types in the content type schema as below:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Usual Zope/CMF/Plone/Archetypes imports
   ...
   from Products.FileSystemStorage.FileSystemStorage import FileSystemStorage
   ...
   my_schema = Schema((
       FileField('file',
       ...
       storage=FileSystemStorage(),
       widget=FileWidget(...)
       ),
       ...
   )
   ...

(b) Using FSS for third party content types as done below for the standard ATFile:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   ...
   from Products.FileSystemStorage.FileSystemStorage import FileSystemStorage
   from Products.ATContentTypes import atct
   ...
   field = atct.ATFile.schema['file']
   field.storage = FileSystemStorage()
   field.registerLayer('storage', field.storage)
   ...

Okay, this works but the pythonic glue of FSS with content types has two
caveats.

At first, we should let the site integrators decide wether he should use
FSS for such or such content type attribute depending on the use, amount
of content (...) of the site without adding lines of Python.

The second one: we depend on the public API of FSS and inners of
Archetypes to do this. This sucks somehow because we plan to transform
the FSS product into a Zope 3 component, this will change the imports.
In addition we use Archetypes low level API (field.registerLayer) to
re-initalize the field storage. That API is subject to changes in the
future as it is not in the public API.

So what? We need to provide a higher level setup for FSS that may
support the furure and we don't want to freeze FSS API and we want to
honour potential Archetypes inner changes.

We can't use ZMI/PMI settings because the storage layer of Archetypes
content must be set at an early stage of Zope startup, means before any
content object is waken up from ZODB.

Using a ZConfig dedicated schema could be an option but ZConfig is not
well suited to such situations.

Bind by configuration
---------------------

Well, the best option is... Creating a ZCML directive for this. Let's
have a look on how to store ATFile content using FSS service from any
"configure.zcml":

.. code-block:: xml

   <configure
      xmlns="http://namespaces.zope.org/zope"
      ...
      xmlns:fss="http://namespaces.ingeniweb.com/filesystemstorage">
     ...
     <fss:typeWithFSS
        class="Products.ATContentTypes.atct.ATFile"
        fields="file" />
     ...
   </configure>

Self explanative, doesn't require any comment for Plone integrators,
doesn't expose or require any specific API.

Now I have defined this, we now need to add the machinery that makes the
glue between that elegant ZCML bunch and the deep inners behind the
scene.

Digging deep into the Zope startup process, notably through Five, and we
can notice that:

-  ``Five`` processes a bunch all "meta.zcml", that define the various
   namespaces and elements that may be used in the "configure.zcml".

-  Then it processes all ``configure.zcml``, those ``configure.zcml`` mainly
   make the high level glue between the various components and products
   of the instance.

-  Finally it processes ``overrides.zcml``, if any that may change
   standard settings provided in the above ``configure.zcml``.

This is a short version and curious people will have a look at
``$INSTANCE_HOME/etc/site.zcml`` to see the details on how to customize the
ZCML setup. Note that with some magic of Five, you don't need to change
anything here if your main zcml files (``meta.zcml``, ``configure.zcml`` and
``override.zcml``) are in a Zope 2 style product.

Okay, aren't you asleep or lost reading this long and boring technical
recipe? No? So let's continue and grab into the depth of the code!

As stated above, I need to define the schema and handler of the element
``<fss:typeWithFSS ...`` from a ``meta.zcml`` and a bunch of Python modules.

Making the ZCML directive
=========================

The meta directive
------------------

In my case, this is a simple element [*]_ and stuff will be somehow
easy since I got the ZCML enlightenment. We can define the such primary
definition in the "meta.zcml":

.. code:: xml
   :number-lines:

   <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:meta="http://namespaces.zope.org/meta">
     <meta:directive
        name="typeWithFSS"
        namespace="http://namespaces.ingeniweb.com/filesystemstorage"
        schema=".zcml.ITypeWithFSSDirective"
        handler=".zcml.typeWithFSS"
     />
   </configure>

.. rubric:: Let's dig into it:

- Line 3: Don't forget to say we're defining a meta, defining its
  namespace.

- Line 5: We define a simple directive, the simplest possible.

- Line 6: The name of our diective.

- Line 7: The namespace for this directive as seen above in the sample ``configure.zcml``.

- Line 8: The schema (read attributes in our case) of that directive is defined by a Zope3 interface.

- Line 9: The handler function that will be invoked for each
  ``<fss:typeWithFSS ...`` directive found at Zope startup.

To keep the things simple, the schema and the handler belong to the same
module, ``zcml.py``

The schema
----------

The people who already made components based on Zope 3 formlib will be
familiar with such notation. A scema is just a Zope 3 interface that
defines in its Python attributes the XML attributes expected from your
directive.

.. code-block:: python

   from zope.interface import Interface
   from zope.configuration.fields import GlobalObject, Tokens, PythonIdentifier
   ...
   class ITypeWithFSSDirective(Interface):
       """Schema for fss:typeWithFSS directive"""

       class_ = GlobalObject(
           title=u'Class',
           description=u'Dotted name of class of AT based content type using FSS',
           required=True)

       fields = Tokens(
           title=u'Fields',
           description=u'Field name or space(s) separated field names',
           value_type=PythonIdentifier(),
           required=True

All these configuration fields are defined in the
``zope.configuration.fields`` package. Have a look to this package to see what
other attribute types I could have used. Note that the attribute types inherit
from zope.schema resources that are familiar to Zope 3 formlib developers.

.. rubric:: Some comments:

-  If your attribute is not required, you may give a default value.
-  You may use a Tokens attribute type where you need multivalued
   attributes from the configuration, as I needed for the "fields"
   attribute. In that case, you define the type for each single value in
   the ``value_type`` keyword argument.

In our case, you can notice the ``class`` attribute of the interface
maps automatically to the ``class`` attribute expected from the
configuration directive. This is a magic that maps all XML attributes
named with a Python keyword as ``class``, "for" and the rest.

The handler
-----------

The handler will be invoked with all directive objectized attributes as
arguments.

.. code-block:: python

   def typeWithFSS(_context, class_, fields):
       """Register our monkey patch"""
       _context.action(
           discriminator=class_.__name__,
           callable=patchATType,
           args=(class_, fields)
           )

   def patchATType(class_, fields):
       """Processing the type patch"""
       for fieldname in fields:
           field = class_.schema[fieldname]
           field.storage = FileSystemStorage()
           field.registerLayer('storage', field.storage)
           LOG("Field '%s' of %s is stored in file system.", fieldname, class_.meta_type)
       return

.. rubric:: The signature of the handler:

-  ``_context``: a context object defined and documented in details in
   zope.configuration.interfaces.IConfigurationContext interface. We'll
   talk about it later.

-  The various attributes in the order of the schema. Optional
   attributes should be passed as keywords args with a default value,
   but we have no optional argument in our example.

You can see that we could immediately patch the content type, using
directly the "patchATType" function body inside the handler.

But it's a much better practice to let the zcml machinery execute as
late as possible that function, and warn on potential conflicts of ZCML
configuration directives.

In that intent, I prefer to register the FSS in the content type
invoking the ``_context.action(...)`` with a discriminator on the class
name that will automatically warn on duplicate FSS patch on the same
content type class.

Have a look at the interface of the ``_context`` object. There are in
lots of other valuables services that you may use in other situations.

Conclusion
==========

I hope this small recipe brought you the "eureka" of the ZCML. As said
earlier in that recipe, you may make more complex ZCML directives, said
"grouping directives". As you got the starter kit in this article about
making a simple directive, you'll get much information on complex
directives looking at the "meta.zcml" from Five or GenericSetup, and
their associated modules.

------------

.. [*] Should we clarify the words used here?

.. [*] Digging the code that handles "meta.zcml", you'll notice that we may define more complex configuration schemas.
