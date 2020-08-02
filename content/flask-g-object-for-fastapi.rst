A Flask "g" object for FastAPI
##############################
:date: 2020-08-02
:author: Gilles Lenfant
:category: Blog
:tags: Python; Tip; Flask; FastAPI
:slug: flask-g-object-for-fastapi
:status: published
:summary: The Flask "g" object is a cool feature, FastAPI has no such feature, but wait...

tl; dr
======

Those who are familiar with Flask are familiar with the ``g`` object that's convenient to have a
"request lifecycle pseudo global" where programmers can store / retrieve arbitrary attributes.

`Here is the doc <https://flask.palletsprojects.com/en/1.1.x/appcontext/#storing-data>`_ for that
``g`` object. Tons of examples of various usages are available at `stackoverflow
<https://stackoverflow.com/search?q=%5Bflask%5D+g>`_ or blog posts (storing a JWT token, the
required API version, ...).

From now, I use FastAPI in place of flask for pure restful API servers. And unfortunately, FastAPI
has not a similar feature. The FastAPI documentation says to use the `request.state
<https://fastapi.tiangolo.com/tutorial/sql-databases/#about-requeststate>`_ object. But this
requires to pass the ``request`` object along in the depth to all callables from the route top
function to every function that needs it.

Good news, this recipe that leverages both the `types.SimpleNamespace
<https://docs.python.org/3/library/types.html#types.SimpleNamespace>`_ and the new stdlib module
from Python 3.7+ `contextvars <https://docs.python.org/3/library/contextvars.html>`_ provides a
``flask.g`` like feature.

The big picture
===============

In short, the ``contextvars`` module provides to programmers a convenient way to have "pseudo
globals" that are shared by coroutines participating to the same asynchronous execution cycle. You
can read better explanations than mmine in the official doc (see the link above) and tons of good
examples `from here <https://www.google.com/search?client=firefox-b-d&q=contextvars+tutorial>`_.

The ``types.SimpleNamespace`` is an arbitrary personal choice for an easy to use attributes
container. Once you'll get the enlightenment of this recipe, you may use a custom object that's
better suited to what you need.

In short, this recipe shows how to:

- Create the request lifecycle shared object.
- (Re)initialize the request lifecycle shared object at each request in a middleware.
- Make a basic usage of that request lifecycle shared object.

If you want to rebuild the demo at home, just create and activate a new Python 3.7+ virtualenv with whatever tool you prefer (virtualenv, venv, pew, - name yours) and issue:

.. code:: console

   pip install fastapi uvicorn requests

Note that ``requests`` is here just to make the demo client easier. You would not need it otherwise.

Now the files...

``requestvars.py``
------------------

The ``requestvars`` module provides the ``contextvars`` bootstrap and the public API for your route
handlers (and app business logic).

[gist:id=2fe530e5a2b90c28608165b5a18afcaf,file=requestvars.py]

.. admonition:: Disclaimer

   I know! "My" ``g`` is a **function** when the Flask ``g`` is just a strange **object** that does
   not need to be called. Any help to fill the gap without a monster machinery is welcome.

``asgi.py``
-----------

Just provides a function that creates our FastAPI ``app`` object. Nothing special. Just notice the ``init_requestvars`` dedicated middleware.

It re-initiallizes the content of our contextvar to an empty ``types.SimpleNamespace`` object. Of
course, you may customize this with a pre-populated namespace with data required by your business
logic, or choose something lese than a ``types.SimpleNamespace`` as free attributes container.

[gist:id=2fe530e5a2b90c28608165b5a18afcaf,file=asgi.py]

``routes.py``
-------------

Just a simple ``GET`` handler at ``/foo`` that requires a ``q`` parameter and returns that
parameters twice. Stupid and useless, its only usage is the use of the ``requestvars.g`` function
that provides the  request lifecycle pseudo-global.

Line 3:
    the usual import as for a global function.

Line 10:
    we add the arbitrary attribute ``blah`` to the request lifecycle pseudo-global which value is
    the ``q`` parameter of the request.

Line 11:
    we call the ``double function`` **with no parameter**

Line 17:
    the ``double`` async function grabs the ``blah`` attribute of our request lifecycle
    pseudo-global and returns it twice.

The other lines do not need comments event to FastAPI noobs.

[gist:id=2fe530e5a2b90c28608165b5a18afcaf,file=routes.py]

``server.py``
-------------

Is just an ordinary minimal ``uvicorn`` server which serves our stupid API on
``http://localhost:8000/foo?q=whatever``. Does not need comment.

[gist:id=2fe530e5a2b90c28608165b5a18afcaf,file=server.py]

``client.py``
-------------

Is just a demo client that consumes our stupid API in an infinite loop, providing as ``q`` parameter whatever string provided as first shell line argument. Example:

.. code:: console

   python client.py whatever

[gist:id=2fe530e5a2b90c28608165b5a18afcaf,file=client.py]

Let's run the demo
==================

Okay now open 3 or more terminals. In each terminal, ``cd`` to the demo directory where you grabbed the above files, and activate the virtual env.

In the first terminal, run the server:

.. code:: console

   python server.py

In the second terminal, run a client with parameter "hop":

.. code:: console

   python client.py hop

You should see...

.. code:: console

   {'result': 'hophop'}
   {'result': 'hophop'}
   ... And so on each second ...

In the second terminal, run a client with parameter "schtroumpf":

.. code:: console

   python client.py schtroumpf

You should see...

.. code:: console

   {'result': 'schtroumpfschtroumpf'}
   {'result': 'schtroumpfschtroumpf'}
   ... And so on each second ...

You may add as many terminals you want and ontinue on with other custom and unique paraméter, and
notice what you can notice with the first two client terminals:

Each request lifecycle has its own values that are propagated through the ``g()`` attributes, that
don't mess with ``g()`` attributes from other requests lifecycles.

Any suggestion to improve this recipe is welcome in comments below.
