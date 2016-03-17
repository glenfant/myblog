Safely replace a Plone member
#############################
:date: 2008-10-17 15:47
:author: Gilles Lenfant
:keyword: Plone
:category: Blog
:slug: safely-replace-a-plone-member
:status: published
:summary: You replace a member by another one in your organisation. Plone has a tool to reflect this in its content.

Hi,

This component replies to a well known use cases and request from our
customers, especially from intranet managers.

How do we do on our Plone intranet when Mr Foo dismisses our company and Ms
Bar is entitled to do his job?

Ms Bruni just married and she's now Mrs Sarkozy. Her login is now c.sarkozy
and she lost the permissions she had on some contents she used to work on. How
shall I handle this? Should I browse in the site finding all her stuffs and
change the sharings, property (...) accordingly?

Some weeks ago, this was in a bunch of code I included in private site
products. Some days ago, I released it as a public component.

Just install
`iw.memberreplace <http://pypi.python.org/pypi/iw.memberreplace>`__,
open its control panel, select the desired options and let it do all the
job - that otherwise would require hours of digging - for you.

Enjoy, and as always, feedback and contributions are welcome.
