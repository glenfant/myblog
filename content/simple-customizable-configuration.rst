A simple customizable configuration
###################################
:date: 2019-03-01 13:01
:author: Gilles Lenfant
:category: Blog
:tags: Python; Tip; Configuration
:slug: simple-customizable-configuration
:status: published
:summary: A simple customizable configuration file

tl; dr
======

Okay okay, okay! If you google "python configuration", you'll get tons of answers with third party nice packages that are capable of managing configuration objects from any format (YAML, JSON, XML, TOML, .ini like, and lots of others) that are stord either in system wide config areas or custom places, with butter and cookies...

The purpose of this post is not to compare all these good but heavy solutions, but to describe a simple solution that:

- Does not need any additional third party package
- Store configuration data in Python files. (Thus if strong security matters, you may find this harmful.)
- Let the user provide a custom configuration in a Python file which globals take over the default configuration values.

The files layout
================

This is a very small and useless app that demonstrates this idea, no more.

.. code:: text

   ├── app
   │   ├── __init__.py         -> Nothing interresting for our demo, it just makes the package
   │   ├── __main__.py         -> Entry point. Only prints options - customized or not
   │   ├── defaultoptions.py   -> The default options and values
   │   └── settings.py         -> Exports the "conf" objects with config data in attributes

``__main__.py``
===============

This is just a "do nearly nothing" application that does not deserve more comments than the... included comments. Just note the ``from  settings import config`` that lets you access to the - maybe customized - configuration options.

.. code:: python

   """
   ===========
   __main__.py
   ===========

   This is just a simple demo that shows how it's simple to use the merged default
   and custom configuration options.
   """
   # Access your config data from this object's attributes
   from settings import config


   def main():
       print("Hello, this is the main entry point.")

       # Use some config options
       print(config.OPTION_1)
       print(config.OPTION_2)
       print(config.OPTION_3)


   if __name__ == "__main__":
       main()

``defaultoptions.py``
=====================

.. attention::

   Do not hesitate to comment in depth each option of a real project and add a copy of this module in your package documentation (this can be easily automated with Sphinx) since the end user needs it to customize the app with his custom options.

This module provides the default options names and values from its globals with uppercase names with no leading underscore. This is just a dummy example.

.. code:: python

   """
   ==============
   defaultoptions
   ==============

   A special module which globals are available through the config namespace unless
   not "forbidden". See the rules in the "settings" module.

   .. warning::

      Do **not** import here from elsewhere in your app unless you may raise a
      circular import error. Anyway, imports from the stdlib or 3rd party package
      are harmless.
   """

   OPTION_1 = "Default value for option 1"
   OPTION_2 = "Any Python object"

   # These options will not be available because...
   stuff = 1  # Starts with a lowercase
   _OPTION = None  # Starts with "_"

   # Anyway you may use "hidden" intermediate objects to build public options
   _intermediate = "anything"
   OPTION_3 = {"key": _intermediate}

``settings.py``
===============

This is the key module - bones and meat - of this blog article. Leveraging the - not very well known - `runpy module <https://docs.python.org/3.6/library/runpy.html#module-runpy>` from stdlib to "parse" both default (``defaultoptions.py`` from above) and custom (if any) configuration files. The resulting configuration data are exposed as attributes of the ``config`` object of this module.

Note that we use below the ``APP_CUSTOM_OPTIONS`` environment variable to tell where's the custom configuration data. Of course you may rename it such it relates to your app name.

.. code:: python

   """
   ===========
   settings.py
   ===========

   The resources provided here provide the merged default and custom options
   in a Namespace named "config". See near the end of this module.

   Example::

      from app.settings import config
      ...
      some_option = config.SOME_OPTION
   """

   import pathlib
   import os
   import runpy
   import types
   import warnings

   # This environment var, if set, should be the path (absolute or relative) to a
   # Python file that overrides some of the default options from
   # "defaultoptions.py".
   CUSTOM_OPTIONS_ENVVAR = "APP_CUSTOM_OPTIONS"


   def keep_upper_names(options_dict: dict) -> None:
       """Remove disallowed option names"""

       def name_rejected(name: str) -> bool:
           """True if not an allowed option name.
           Legal names are:
           - All uppercases with potential "_" or [0..9] inside
           - Don't start with "_"
           """
           return name.startswith("_") or name.upper() != name

       # Remove "illegal" option names.
       for name in list(options_dict):
           if name_rejected(name):
               del options_dict[name]


   # This is the default options dict
   default_options = runpy.run_module("defaultoptions")
   keep_upper_names(default_options)

   # This will build the "custom_options" dict
   custom_options = {}
   custom_options_file = os.getenv(CUSTOM_OPTIONS_ENVVAR)
   if custom_options_file:
       custom_options_file = pathlib.Path(custom_options_file)
       if custom_options_file.is_file():
           custom_options = runpy.run_path(custom_options_file)
           keep_upper_names(custom_options)
       else:
           warnings.warn(
               f"No {custom_options_file} found. Fix or remove env var {CUSTOM_OPTIONS_ENVVAR}",
               ResourceWarning,
           )

   # And finally the object that exposes the custom options merged with the default
   # ones as attributes.
   config = types.SimpleNamespace(**{**default_options, **custom_options})

Okay, time for the demo
=======================

If you copied exactly the files layout and contents, you may proceed to the demo, otherwise you should adapt what follows to your app layout and names.

- cd to the parent directory (the one that contains the ``app/`` directory) and execute the command:

.. code:: console

   python app

This should display:

.. code:: text

   Hello, this is the main entry point.
   Default value for option 1
   {'key': 'anything'}

You have seen the default values of three options. Now let's start a custom configuration. Create in the same directory a ``customoptions.py`` file with only this line:

.. code:: python

   OPTION_1 = "Custom value for option 1"

We can now "tell" the app to use the custom options redefined in this file:

.. code:: console

   APP_CUSTOM_OPTIONS=customoptions.py python app

Now this displays:

.. code:: text

   Hello, this is the main entry point.
   Custom value for option 1
   Any Python object
   {'key': 'anything'}

As you can notice, this only changed the value of ``OPTION_1`` when the other options keep their default value.

.. attention::

   The examples work as is with Python 3.6 and up. Using an older Python version down to Python 2.7 may require some changes (no pathlib, fo f-strings, etc.)
