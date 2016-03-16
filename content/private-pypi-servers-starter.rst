Private Pypi servers - 1 - Forewords
####################################
:date: 2013-08-28 21:01
:author: glenfant
:tags: Plone, Python
:slug: private-pypi-servers-forewords
:status: published
:summary: Presentation of the private PyPI servers competition.

Intended audience
=================

We assume most of you readers are already familiar with the public Pypi
- formerly known as Cheeseshop - server.

As user, you already know how to search and browse on
`Pypi <https://pypi.python.org/pypi>`__ then install the packages that
fit with your app.

We also assume that pip, easy_install and zc.buildout have no major
secret for you.

In addition, you are supposed to know how to tweak correctly the
setup.py of your personal package - with appropriate metadata - such you
can deploy this package on Pypi such others - or yourself - can install
it with the various installation tools mentioned in previous paragraph.

If not, please have a look at the official documentations for these
tools :

-  setuptools: http://pythonhosted.org/setuptools/index.html

-  pip: http://www.pip-installer.org/en/latest/

-  zc.buildout: https://pypi.python.org/pypi/zc.buildout and
   http://www.buildout.org/en/latest/

Why a private Pypi server?
==========================

Most of professional Python developers work in companies or as
freelances and contribute to commercial and private projects which
results of clever combination of publicly available packages (lxml,
SQLAlchemy, …) and private package that leverage the various domains of
your applications features.

In order to carry on using your favourite Python packaging and
installation software factory tools, you need of course to have a
private repository of packages to build your private applications while
keeping the public packages you need in their own respective repository
(usually the Pypi or one of its official clones).

The compared features
=====================

Software foundations
--------------------

Of course, you’re not supposed to do anything else than running the
installation recipe of your favourite Pypi server. But you may prefer
such or such base framework if you want to contribute later, or you may
have some pain to install the required database, or other requirement,
these information are here for this.

Base frameworks
---------------

I’m not trying to open a flame on the various base frameworks used by
our various Pypi clones, but, as programmers, you may prefer such or
such framework if you want to contribute or fix bugs of your favorite
Pypi server.

Database
--------

Some of the nominees required a 3rd party database. Is this database
compatible with your company policy, or with the target system you want
to dedicate to your Pypi server ?

Installation
------------

Some words about installation. But from the easiest to the most complex
of our nominees, installation and basic customization are usually easy.

Documentation, Community support
--------------------------------

As you are going to choose, perhaps for a long period, an application
that is actively maintained

About this, some private Pypi servers have been discarded from this
article because these are not actively maintained anymore.

Even if most of us are Python experts, and are supposed to feel
comfortable on Unix admin and databases, we don’t like to grep the code
when the documentation is missing or is too spartan. And a good,
structured and exhaustive documentation denote high quality products.

UI
--

Some of the nominees have nearly no Web UI, you may anyway not need an
UI if you have few packages.

A Web UI may be useful for things like changing security settings on a
particular package, changing its keywords or some features of its
documentation, removing or hiding deprecated versions, ...

Proxying
--------

Proxying the public Pypi or another public server may be useful.

-  Your proxy can distribute public packages when the official Pypi is
   down.

-  You work behind your company’s proxy and this makes a mess to
   easy_install from the official Pypi.

Some of the competitors described in this article may contain clones of
packages that are distributed by the official Pypi. These clones
packages may be updated periodically through a “cronned” query.

Users management and privileges
-------------------------------

Your IT infrastructure has already a common authentication source (LDAP
or like) and you don’t want to mess your users with an additional
credential to remember ?

You want to provide these users fine grained privileges on various parts
of your private Pypi, either on a per user base or through groups and
roles ?

If your private Pypi server has multiple repositories (see below), you
want to grant or disallow distinct groups of users or individual users
in a per repository policy ?

Custom security policies
------------------------

Ah, the Pypi server you have been dreaming of is almost what you need
but the built in security policy does not comply exactly your
requirements. You need something fine grained that lets you define
custom roles with dedicated and maybe localized permissions.

Multiple repositories
---------------------

With one server instance you may publish two or more repositories with
their own security policies thanks to the above mentioned users
management and privileges. This may be useful if you need a private and
a public repository, or if you need to give to your various customers or
partners access to their dedicated packages.

Upload with setuptools
----------------------

If your private Pipi server has this feature, you could register and
upload your private Python packages with the usual setup respective
commands :

python setup.py sdist register [options]

python setup.py sdist upload [options]

If you prefer a more minimalistic Pypi server that has not this feature
(say a simple Apache static distributed directory) , you should :

python setup.py sdist

scp dist/foo-1.2.3.tar.gz myself@apache-pypi:/home/distros/foo/

XMLRPC and REST/JSON support
----------------------------

This is not an essential feature though none of pip,
setuptools/easy_install or zc.buildout seem to use this exploration
feature that’s provided by the official Pypi.

Read http://wiki.python.org/moin/PyPIXmlRpc and
http://wiki.python.org/moin/PyPIJSON .

I could add that I never needed this for in the Python projects I’ve
been working on. But perhaps you care about this. That’s why I made a
small test script to run against each nominee.

The nominees
============

Apache
------

Yes, you can use a pure Apache with dedicated configuration to make your
private Pypi server. This is a very reliable solution that just needs a
dedicated configuration section. Preferably for a dedicated virtual
host, or several virtual hosts since you may have multiple repositories
for one Apache instance. Of course, there’s no upload capability, nor
Web dedicated UI, unless you call browsing the simple index an UI.

Pypi itself
-----------

If the official Pypi as at http://pypi.python.org is exactly what you
need, thats perfect. This software is open source and may be installed
in your private servers or cloud.

Plone Software Center
---------------------

The venerable Plone is a modern, full featured non opinionated CMS with
a modern UI. Products.PloneSoftwareCenter is a rich add-on for Plone
that lets you add to a company intranet the features of a Pypi server,
with a rich UI, setuptools upload capability, and a documentation area.

You may add Products.Poi to add trackers to your package areas.

But Plone is some kind of “monster” that provides out of the box lots of
features that are not in the domain of a Pypi server requirements. In
addition, a Plone app is resources expensive and requires more admin
monitoring than other solutions. Your IT department executives would not
like this.

For the ones who care about corporate theming, PSC can be themed through
the usual Plone theming service - read Diazo based themes with the
latest Plone versions.

mypypi
------

mypypi is a full featured Pypi server built on top of Zope 3. It
provides a spartan and old style but fully functional and nearly
complete UI.

It leverages the security features and the user sources interfaces of
Zope 3 such you may customize the user sources and security policy to
whatever you may prefer if you can understand what is ZCML and if you
know how to add custom user sources available in the Zope ecosystem.

crate.io
--------

crate.io is the newcomer in the gang and benefits of a very positive
buzz. Its UI is resolutely modern in line with the new twitter bootstrap
trend. Its framework leverages asynchronisms through Celery that
supports heavy time consuming tasks, and thus helps to have a fast and
fluid UI.

Meet its public repository and have an account at http://crate.io

devpi
-----

inupypi
-------

pypiserver
----------

localshop
---------

simplepypi
----------

Hey, wait! There are other ones
-------------------------------

Why do I not tell any word about them ?

The answer is simple : the other Pypi private server software (known by
me) seem to be some kind of abandonwares. But if you want to make a test
drive of these and make an opinion...

-  ClueReleaseManager: https://pypi.python.org/pypi/ClueReleaseManager

-  EggBasket: http://trac.chrisarndt.de/code/wiki/EggBasket

-  haufe.eggserver: https://pypi.python.org/pypi/haufe.eggserver

-  chishop: https://github.com/ask/chishop

-  scrambled: https://pypi.python.org/pypi/scrambled

If you’re a contributor of one of the above mentioned softwares, and I
missed something. Or if you know of another private Pypi server software
that’s not mentioned in this article, please let me know what I missed
or where I’m wrong. I’ll update this article accordingly. But, remember,
this is not a troll playground :D
