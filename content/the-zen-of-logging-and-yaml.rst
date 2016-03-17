The zen of logging and YAML
###########################
:date: 2012-12-22 15:07
:author: Gilles Lenfant
:tags: Python
:category: Blog
:slug: the-zen-of-logging-and-yaml
:status: published
:summary: A Python logging configuration in YAML

Python 2.7 and 3.2 come with a new way to configure the Python logging
services with a standard dict. Is there a better way to let an user
provide a dict than YAML ?

ConfigParser ? Uh ! Not sure. In addition, YAML provides OOTB lists,
aliases, and even arbitrary Python objects.

Just having got the zen of complex logging and YAML, I write this self
explanatory recipe for my memory and anyone who want to configure a
complex logging with only some lines of Python. Any comment, question,
improvement suggestion is welcome.

[gist:id=4358668]
