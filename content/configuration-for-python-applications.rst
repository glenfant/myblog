Configuration for Python applications
#####################################
:date: 2016-03-26 10:57
:author: Gilles Lenfant
:tags: Python
:category: Blog
:slug: configuration-for-python-application
:status: draft
:summary: Different ways to configure your Python applications

Abstract
========

Medium or big sized applications need flexibility in order to allow facing various user requirements. Of course, you could - and you certainly should - use `argparse <https://docs.python.org/3/library/argparse.html>`__  from stdlib or `click <http://click.pocoo.org/5/>`__ add-on to let the user provide his / her preferences and targets.

But this is somehow annoying when the user needs to always repeat the same options set when he works all day long within the same project context, and uses the same looooong command lines.

That's why most flexible applications let the user choose his preferred options in a configuration file. And plenty of solutions are available to Python application developers.

I'll discuss here about some of the most popular solutions, and expose their respective benefits and drawbacks.

Intended audience
=================

This blog article is for an audience of beginners with a couple of weeks of Python practice.

The stdlib solutions
====================

The main advantage of using a solution exclusively based on resources from stdlib are:

- Of course you minimize your project requirements
- You're sitting on giant shoulder, using popular configuration formats and - almost - bug free solution.

configparser
------------

I won't go in deep in `configparser <https://docs.python.org/3/library/configparser.html>`__ since it is explained in details in the standard documentation.

.. hint::

   I'm talking here about the ``configparser`` that ships with Python 3.x, the one that ships with Python 2.6 or Python 2.7 is slightly different. If you want the Python 3.x features of ``configparser`` in your Python 2.x application, you may add the `configparser2 <https://pypi.python.org/pypi/configparser2/>`__, a backport of Python 3.x ``configparser`` to Python 2.x, in your application requirements.

`configparser <https://docs.python.org/3/library/configparser.html>`__ is the most popular - configuration file utility. It uses the well known ``.ini`` file format popularized by Windows.

.. code-block:: ini

   [foo]
   # A comment line
   database = mydb
   option2 = 3000
   pidfile = /var/lock/myapp.pid

   [bar]
   option1 = test_${foo:option1}

.. list-table:: Summary
   :header-rows: 1
   :widths: 35 65

   * - Feature
     - Comment
   * - Data model
     - Nested on 2 levels: sections and options, with limited mapping protocol
   * - Parsed data types
     - Strings only. You need to convert to ``int``, ``float`` or ``bool`` at parse time. Custom converters are possible by subclassing the parser.
   * - Interpolation
     - Yes: global and per section interpolations are possible



XML
---

Windows registry
----------------

This is the preferred way for Windows applications. The registry is some kind of persistent hierarchical key/value(s) database with a secured access, in which most Windows applications store their user preferences. Of course you should not opt for this solution if you want to distribute a cross-platform application.

Windows comes with the ``regedit.exe`` application that lets you tune applications as you want. But be careful when using this utility as computer administrator. You may corrupt other applications or kick yourself off the system.

Mac OSX Plist
-------------

As for above mentioned Windows registry, you may choose this solution for pure OSX applications.

The add-on solutions
====================

Some add-on solutions provide more flexible or powerful

What about the others
=====================

| "Hey man! You forgot to talk about xxx and yyy"

Yes perhaps I'm not aware of these solutions, but let me tell you some words about those I didn't mention and do not intentionally, and I do not recommend. For other solutions, you may add some words in the comments of this post.

JSON
----

Yes JSON files may be used to configure your application. JSON provides the same data structure as the ones provided by YAML, and is popular in the NodeJS world, but:

- There's no standard for comments in JSON, you cannot document your configuration file with the Python OTB JSON support.
- JSON has not the rich substitution and aliasing features of YAML.

So you may use JSON for applications with few configurable data, but prefer YAML or another one if you need flexibility or support for larger configuration files.


