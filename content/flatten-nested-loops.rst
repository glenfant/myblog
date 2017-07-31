"Flatten" nested loops
######################

:date: 2017-07-31 17:01
:author: Gilles Lenfant
:category: Blog
:tags: Python; Tip
:slug: flatten-nested-loops
:status: published
:summary: One loop in place of x nested loops

Nested loops are a common pattern in programmation in most programming languages. In Python,
nested loops that have a long body must indent at each loop, that's wastes screen space and hides
the fact the code is in an unique loop.

In addition, ``break`` statements in the outermost loop will continue with the next parent loop.
If the intent is to break the outermost loop, the programmer needs to include these nested loops
in an outer ``try ... except`` structure that adds one more indentation level, or add a loop logic control.

This recipe can be used in most cases you need nested loops that are merged in one. The "black
magic": merge the looping logic in a `generator expression
<https://www.python.org/dev/peps/pep-0289/#reduction-functions>`_.

Before:

.. code-block:: python

   must_break_all = False
   for obj1 in iterable1:
       if must_break_all:
           break
       for obj2 in iterable2:
           if must_break_all:
               break
           for obj3 in iterable3:
               lots_of_data_processing()
               if we_must_stop():
                   must_break_all = True
                   break
                other_data_processing()
   # End all iterations
   doing_something_else()

Ugly, isn't it?

In place of this I prefer use a generator expression that merges the looping logic, like this:

.. code-block:: python

   merged_looping = ((obj1, obj2, obj3)
                     for obj1 in iterable1
                     for obj2 in iterable2
                     for obj3 in iterable3)
   for obj1, obj2, obj3 in merged_looping:
       lots_of_data_processing()
       if we_must_stop():
           break
        other_data_processing()
   # End all iterations
   doing_something_else()

And yes, you can put any number of consistent ``for`` expressions in one generator expression.

.. warning:: **Exhausted generator**

   You can't re-use ``merged_looping`` as is after the last line of this example because it is
   potentially exhausted.
