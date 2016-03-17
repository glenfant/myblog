Changing workflow state  - quickly - on CMF/Plone content
#########################################################
:date: 2010-04-02 08:31
:author: Gilles Lenfant
:tags: Plone, Zope 2
:category: Blog
:slug: changing-workflow-state-quickly-on-cmfplone-content
:status: published
:summary: It is sometimes useful to change the workflow state of a content item without invoking transitions ans their side effect

The issue with workflow states and transitions
==============================================

The tip of the gruik [*]_...


I have been investigated some months ago with `Encolpe Degoute
<http://encolpe.wordpress.com/>`__ on how to set a workflow state on a content
when the workflow is DCWorkflow powered (Plone of course). Things are not that
simple since DCWorkflow does not provide a public API for this. Instead, we
must execute the various transitions that are slow and may trigger unwanted
events.

.. admonition:: Attention

   This small scripts uses deep inners private API of DCWorkflow (yeah, that's
   evil, but...) and makes the expected job:

-  Sets the workflow state of a content to whatever state without
   executing any transition

-  Sets its security martix as expected

-  Reindexes content security

Here is the baby... In the hope it will be useful to others and maybe
get improvements...

It has been used in many Plone apps and migration utilities.

--------------

.. code-block:: python

   from Products.CMFCore.utils import getToolByName
   from DateTime import DateTime
   def sample(folderish):
       folderish.invokeFactory(type_name='Document', id='blah', title="Blah")
       blah = folderish['blah']
       changeWorkflowState(blah, 'published', comments="No comment")
       return

   def changeWorkflowState(content, state_id, acquire_permissions=False,
                           portal_workflow=None, **kw):
       """Change the workflow state of an object
       @param content: Content obj which state will be changed
       @param state_id: name of the state to put on content
       @param acquire_permissions: True->All permissions unchecked and on riles and
                                   acquired
                                   False->Applies new state security map
       @param portal_workflow: Provide workflow tool (optimisation) if known
       @param kw: change the values of same name of the state mapping
       @return: None
       """

       if portal_workflow is None:
           portal_workflow = getToolByName(content, 'portal_workflow')

       # Might raise IndexError if no workflow is associated to this type
       wf_def = portal_workflow.getWorkflowsFor(content)[0]
       wf_id= wf_def.getId()

       wf_state = {
           'action': None,
           'actor': None,
           'comments': "Setting state to %s" % state_id,
           'review_state': state_id,
           'time': DateTime(),
           }

       # Updating wf_state from keyword args
       for k in kw.keys():
           # Remove unknown items
           if not wf_state.has_key(k):
               del kw[k]
       if kw.has_key('review_state'):
           del kw['review_state']
       wf_state.update(kw)

       portal_workflow.setStatusOf(wf_id, content, wf_state)

       if acquire_permissions:
           # Acquire all permissions
           for permission in content.possible_permissions():
               content.manage_permission(permission, acquire=1)
       else:
           # Setting new state permissions
           wf_def.updateRoleMappingsFor(content)

       # Map changes to the catalogs
       content.reindexObject(idxs=['allowedRolesAndUsers', 'review_state'])
       return

--------------

Pros
====


-  It's damn fast. Consider using changeWorkflowState if you need to set
   the workflow on a huge set of contents in one transaction. Read a
   content migration or a bulk content creation.

-  You can set the workflow state you want, including a state that's no
   in the workflow associated with the content ;o)

Cons
====

- Doesn't use legacy API. So this may or may not work with future versions of
  DCWorkflow.

- Doesn't use the transitions. This is an intentional feature forspeeding up
  all this. As a consequence, no transition script or eventis triggered. But
  this is perhaps not recorded in workflow history. Honestly this is not an
  issue for my use case.

As a counterpart, there's no control on the validity of the state value in the
context (global workflow or placeful workflow). Buggy user code may issue
content on which no workflow transition is possible.

--------------

.. [*] French speaking readers will understand. For others, "Gruik" is the sound of the pig.
