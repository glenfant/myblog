Archetypes sucks...
###################
:date: 2008-05-09 15:04
:author: glenfant
:category: Blog
:tags: Plone
:slug: archetypes-sucks
:status: published
:summary: Hearing bad feedbacks from Archetypes. WTF?

Eh, not my personal opinion but...

That's what we can read in some posts and blogs. So, why does AT sucks
according to these opinions?

-  It's old style python (read mostly plain 2.1 python) and doesn't use
   the latest features that came up to Python 2.4 (decorators, misc new
   style classes features...).
-  There's no out of the box support for repetead fields or groups of
   fields (read "we can't add n files or images")
-  AT is uselessly noisy, and it's code is now as messy as obese.
-  AT is slow, more specifically for authors, and is a major cause of
   Plone lazyness.
-  AT APIs are sometimes complicated. We use
   "content.getField('foo').set(content, value)" when Python 2.4 could
   let us just type "content.fields.foo = value" or better "content.foo
   = value".
-  AT is not Zope3 "ish", or does the minimal stuff to run within Plone
   3. And yes, it uses always the old style Zope 2 interfaces, CMF skins
   layer, nested complex ZPT macros where viewlets could do better job.
-  The set of metadata that ship with AT is not really extensible or
   replaceable though it's named ExtensibleMetadata.

So... Let's **KILL** Archetypes! Yes, and what else?

Okay there's new kids on the block. There's lot of buzz around good
newcomers in the field of AT, like the new plone base contents (see the
`plone.app.content <http://pypi.python.org/pypi/plone.app.content>`__
egg) you can use if you don't need advanced features.

Or you could wait for the promising new framework
`Devilstick <http://devilstickproject.net/>`__ that will let us define
the data model with XML.

Just don't forget that if Plone ships with a nice collection of content
types, has so many third party content types and rich services, if Plone
is often referred as the best open-source CMS, if you can sell Plone
based competitive solutions to your customers you just need to say
"**Thank you so much Archetypes developers**".

In addition, most (all?) of above listed issues of today's Archetypes
can be fixed in the future without breaking support for actual content
types.

Due to so many skilled developers and rich solutions Archetypes is here
to stay for years and years. Yeah!
