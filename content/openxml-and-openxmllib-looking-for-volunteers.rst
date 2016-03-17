OpenXml and openxmllib - looking for volunteers
###############################################
:date: 2008-11-21 14:50
:author: Gilles Lenfant
:tags: Plone
:category: Blog
:slug: openxml-and-openxmllib-looking-for-volunteers
:status: published
:summary: If tyou care of MS 2007 or later support in Plone...

Abstract
========

`openxmllib <http://code.google.com/p/openxmllib/>`__ is a pure Python package
built on lxml that parses an ECMA373 office file (read ``*.docx``, ``*.pptx``,
``*.xlsx`` recorded from MS Office 2007). It can actually extract - very fast
- the indexable words from an MS Office 2007 document. It may be used from any
Python app, even from others (Java, PHP, C++ ...)

`Products.OpenXml <http://plone.org/products/openxml>`__ is a component for
Plone 2.5 -> 3.2 that registers the MIME types and icons for the known
extensions for these office files and provides transform rules to indexable
text, such MS Office 2007 documents in ATFile or any content type with a
searchable FileField are indexed.

Both are avalaible at the cheeseshop.

Future directions
=================

Yeah, those babies make satisfying job at the moment, I have not enough room
to copy the testimonies of satisfied users. But users want more...

Have real plain text
--------------------

openxmllib actually provides all words from a document. This is very fast
because some XPath expressions make the job. But when the result is
appropriate for indexing, it is not human friendly. The words are returned in
any order and there's no way to understand what's written.

Have HTML preview
-----------------

Yes, previews of office documents in a Plone site are great. ARFilePreview
shows some of what I want to do: having a nice HTML document, visually as
close as possible from the printed document.

Volunteers?
===========

Unfortunately, I have not much time to spend for this, and the ones who asked
these features didn't want to participate or fund my work. You are interrested
for adding these features, please let me know. Skills in XSLT and in the
ECMA373 standard are required for this.

Many thanks by avance.
