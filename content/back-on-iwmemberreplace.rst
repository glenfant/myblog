Back on iw.memberreplace
########################
:date: 2009-03-08 14:36
:author: Gilles Lenfant
:category: Blog
:tags: Plone, Zope 2, Zope 3
:slug: back-on-iwmemberreplace
:status: published
:summary: Bulk attributing content to members

I blogged some months ago about `iw.memberrreplace <http://plone.org/products/iw-memberreplace/>`__
in `this page <{filename}safely-replace-a-plone-member.rst>`_. In some words,
iw.memberreplace provides a tool that clones the security features of an unser
to another one (ownership, DC creator, sharings, group membership). No more
hassle digging around huge Plone site and hundreds of clicks to do this.

Last week, I read a conversation with `John Stahl and Mustapha
Benali <http://n2.nabble.com/Re%3A-what%27s-up-with-plone.app.changeownership-%21-%21-tp2416270p2416270.html>`__
about the `PLIP 185 <http://plone.org/products/plone/roadmap/185/>`__,
and realized that this PLIP is almost iw.memberreplace (or the
opposite).

So I spend a couple of hours on that component to add the last details
on that component. Et voilà, the last release of iw.memberreplace
(1.0.0-RC1) fulfills now that PLIP: the original member can now be
removed - if defined in a mutable users source.

I swear that in the future, I will read the open PLIPs before creating a
new component ;o)

Enjoy...

.. figure:: {filename}/images/memberreplace-control-panel.png
   :alt: The control panel

   The control panel
