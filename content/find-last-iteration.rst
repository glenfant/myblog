Find the last iteration
#######################
:date: 2017-09-16 13:01
:author: Gilles Lenfant
:category: Blog
:tags: Python; Tip
:slug: find-the-last-iteration
:status: published
:summary: Find the last iteration on any iterable object

It's sometimes useful to determine where's the last iteration on an iterable object.

Doing this on a sized object is pretty easy. You just need to get the ``len()`` of the container object you're looking over, learn ``enumerate`` and just:

.. code:: python

   obj = (1, 2, 3)
   obj_len = len(obj)
   for i, item in enumerate(obj):
       do_stuff_with(item)

       # Special for last item
       if i == obj_len - 1:
           do_play_with(item)

That's OK in situations where you can count the iterations before entering in a loop, but what if the ``obj`` your code is looping over is not `Sized <https://docs.python.org/3/library/collections.abc.html#collections.abc.Sized>`_?

This generator comes to the rescue and will notify the last iteration over any iterable object.

.. code:: python

   import collections

   def notify_last_item(iterable):
       """Iterates over an iterable of items and yields a 2 tuple contaning
       (is_last, item).  `is_last` being True when last item is yielded

       :param iterable: iterable or iterator
       :yield: (is_last, item) tuple

       >>> seq = range(4)
       >>> list(notify_last_item(seq))
       [(False, 0), (False, 1), (False, 2), (True, 3)]
       """
       # Belt + braces
       if not isinstance(iterable, collections.Iterator):
           iterable = iter(iterable)

       # Pull 1st value
       last = next(iterable)  # Pull 1st value

       # Run iterator to exhaustion
       for value in iterable:
           yield False, last
           last = value

       # Report the last value
       yield True, last

Now for a simple demo:

.. code:: python

   obj = iter(range(5))  # Not sizeable
   for is_last_item, item in notify_last_item(obj):
       print(is_last_item, item)

   # Outputs:
   # False 0
   # False 1
   # False 2
   # False 3
   # True 4

Any comment for improvements or others are welcome...
