Awaiting a blocking callable
############################
:date: 2020-08-04 13:01
:modified: 2020-08-04 13:01
:author: Gilles Lenfant
:category: Blog
:tags: Python; Tip; Asyncio
:slug: awaiting-a-blocking-callable
:status: published
:summary: Transform a regular callable (function / method) into an async coroutine

tl; dr
======

Working with frameworks that leverage the ``asyncio`` paradigm is now familiar to lots of Python
programmers with popular asynchronous frameworks like FastAPI, Faust, Trio (name yours...).

We need sometimes to use good libs that do not (yet ?) leverage the - not so - new ``asyncio`` way,
and provide only blocking APIs. Think about SQLAlchemy, or others. 

Using such services from a coroutine under event loop control will lock the event loop while
executing thus yield a performance issue.

Hopefully the stdlib provides the `concurrent.futures
<https://docs.python.org/3/library/concurrent.futures.html>`_ package that let us work around this
annoyance and make a coroutine from a blocking function or method.

The code
========

[gist:id=24dc52bb3fe2c39d20c14369a86c43bf,file=call_blocking.py]

The demo
========

Just paste this code under the above one...

[gist:id=24dc52bb3fe2c39d20c14369a86c43bf,file=demo.py]

About the pool executor
=======================

You may choose the ``_executor`` being either ``None``, a ``ThreadPoolexecutor`` or a
``ProcessPoolExecutor`` instance. Just read the doc of ``concurrent.futures`` to choose the best
suited. And read the `Drawbacks`_ below.

Pool executor constructor take an optional ``max_workers`` argument you should perhaps tune to
obtain the best possible performances.

My hints: choose a ``ThreadPoolExecutor`` for I/O expensive functions, and a ``ProcessPoolExecutor``
for heavy computation callables.

Drawbacks
=========

Using threads
-------------

You must be careful when playing with shared objects that could be modified by your blocking code
and coroutines under event loop control. Avoid this when possible, or use locks.

In addition lots of trird party packages expose resources that are not "thread safe", thus cannot be
invoked with this recipe.

Using processes
---------------

Processes do not share any global. Blocking code and coroutines must communicate via a
``multiprocessing.Queue``. That's not very comfortable.