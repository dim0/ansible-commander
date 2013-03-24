API Guide
=========

This document describes how to do nearly everything in Ansible commander via the REST API.

To begin,  you should have set up Ansible Commander (see SETUP.md) and created at least one Django super user.
To do this from the development project, run "make adduser".

For the purposes of this guide, we will assume the superuser username and password is admin/admin.

Conventions
===========

* Ansible Commander uses a standard REST API, rooted at /api/v1/ on the server.
* All data is JSON.  You may have to specify the content/type on POST or PUT requests accordingly.
* All URIs should end in "/" or you will get a 301 redirect.

Time to get started.

Aside: Django Admin
===================

When working with REST objects it is often helpful to use the Django admin interface to pre-create objects,
and then retrieve collections of objects with GET request to look at their structure.  This will help
users understand how to create new objects as well as how to edit them.

Aside: Read Only Fields
=======================

Certain fields in the REST API are marked read only.  These usually include the URL of a resource, the ID,
and occasionally some internal fields.  For instance, the 'created_by' attribute of each object indicates
which user created the resource, and can not be edited.

A Prelude: Workflow
===================

Assume you are starting out with a blank Ansible Commander instance, and don't intend to use the GUI.
What sort of REST operations do you need to perform to seed everything out and deploy your first
playbook entirely via web services?  It would look something like this.

Create Users and Organizations
------------------------------

 * Confirm your super user account at /api/v1/me/
 * Create some organizations at /api/v1/organizations/
 * Create some users at /api/v1/users/
 * Add some users to some organizations at /api/v1/organizations/X/users/
 * Add some users to be admins of those organizations at /api/v1/organizatoins/X/admins/
 * At this point, use your org admin account, instead of your superuser account, if you wish

Build Out Inventory
-------------------
 
 * Create an inventory resource at /api/v1/inventories/
 * Create some host records at /api/v1/hosts/
 * Add the host to inventory at /api/v1/inventories/X/hosts/
 * Create some group records at /api/v1/projects/
 * Add the group to inventory at /api/v1/inventories/X/groups/
 * Create some variables at /api/v1/variables/
 * Add some variables to a host at /api/v1/hosts/X/variables/
 * Add some variables to a group at /api/v1/groups/X/variables/
 * Add a subgroup to a group at /api/v1/groups/X/children/

Set Up Projects and Teams
-------------------------

 * Create some teams at /api/v1/teams/
 * Create some projects at /api/v1/projects/
 * Assign some projects to one or more teams at /api/v1/teams/X/projects/

Save Login Credentials and Grant Role (Team) Based Permissions
--------------------------------------------------------------

 * Create some login credentials at /api/v1/credentials/
 * Assign credentials to some teams at /api/v1/teams/X/credentials/ OR
 * Assign credentials to some users at /api/v1/user/X/credentials/ (no fancy priveledges required)
 * Create a permission tuple to allow a user or project to be used with an inventory source at /api/v1/permissions/
 * Permission tuples can allow execution, dry run execution, or inventory editing.

Launch Playbooks and View Results
---------------------------------

 * Create a launch job request by posting project, permission, and credential to /api/v1/events/
 * Monitor the job results at /api/v1/launch_results/X
 * See the history of runs on each host at /api/v1/hosts/X/events/ or /api/v1/groups/X/events/ or /api/v1/inventories/X/events/

Audit API based Activity, Search For Resources
----------------------------------------------

 * Apply tags or see applied tags on any resource at /api/v1/RESOURCE/X/tags/
 * View audit trail information on any resource change at /api/v1/RESOURCE/X/audit_trail/



Working With Users

==================

After a fresh install, there should be no organizations and only the superuser.

Since we're explaining our first resource, we'll be a bit more verbose with the user
information than with some other REST resources.

Listing Users
-------------

We will pay special attention to this first access request, as any list view looks basically
the same.

    curl http://admin:admin@127.0.0.1:8013/api/v1/users/

    {
        "count": 1, "next": null, "previous": null,
        "results": [
            {
                 "url": "/api/v1/users/1/",
                 "id": 1, "username": "admin",
                 "first_name": "",
                 "last_name": "",
                 "email": "root@localhost.localdomain",
                 "is_active": true,
                 "is_superuser": true,
                 "related": {
                     "admin_of_organizations": "/api/v1/users/1/admin_of_organizations/",
                     "organizations": "/api/v1/users/1/organizations/",
                     "teams": "/api/v1/users/1/teams/"
                 }
             }
        ]
    }

Notice that the requests are paginated, so you may have to access additional URLs if 'previous' and 'next'
are set to access the full collection.

You will also see 'related' URLs on each object, which tell you from any point in the API what resources
you can get to from a particular resource.

Adding Users
------------

To add a user, just POST to the users collection:

    curl -X POST -d @input http://admin:admin@127.0.0.1:8013/api/v1/users/

    {
         "username" : "foo", "password: "foo"
    }

And optionally specify other fields.  Super users or organization admins can create users.  We'll learn more about
organizations shortly!

Getting a User
--------------

As you would expect, a user, superuser, or organization admin can retrieve the record of a user directly via:

    curl http://admin:admin@127.0.0.1/api/v1/users/1/

And recieves something very much like this:

    {
        "url": "/api/v1/users/1/",
        "id": 1, "username": "admin",
        "first_name": "",
        "last_name": "",
        "email": "root@localhost.localdomain",
        "is_active": true,
        "is_superuser": true,
        "related": {
            "admin_of_organizations": "/api/v1/users/1/admin_of_organizations/",
            "organizations": "/api/v1/users/1/organizations/",
            "teams": "/api/v1/users/1/teams/"
        }
    }


Deleting Users
--------------

In ansible commander, nothing is truly deleted, objects are only set inactive and renamed.  This allows recovery
of those objects using the Django administrative interface or the database command line.

To delete an object, just DELETE to a resource, like so:

    curl -X DELETE http://admin:admin@127.0.0.1:8013/api/v1/users/2/

Only a user's organization admins, or a superuser, can mark a user as deleted.

Updating Users
--------------

A user may update only his password, and an organization admin or superuser can update a lot more about the
user.  To update a user, just PUT to the resource, like so:

    curl -X PUT -d @input http://admin:admin@127.0.0.1:8013/api/v1/users/2/

    {
         'password': 'new_password'
    }

Organizations
=============

Organizations are the basic unit of multi-tenancy and access in Ansible Commander.

At the basic level, when a user is created, he should then be added to one or more organziations.

These may represent concepts like "Engineering" or "Finance".

Under each organization, there will also be multiple teams, like "Engineering QA Team", or "Engineering Release Team".

Organizations also have admin users (which can be assigned by the super user or other organization admins) whom also
have most of the powers of a superuser to users inside that organization.

Listing Organizations
---------------------

GET /api/v1/organizations/

Editing Organizations
---------------------

PUT /api/v1/organizations/1/

Adding users to an organization
-------------------------------

POST the data you recieved from GET /api/v1/users/X/ to /api/v1/organizations/Y/organizations/

Similarly, you can list users of an organization if you are an org admin or superuser with:

GET /api/v1/organizations/X/users/

Adding admins to an organization
--------------------------------

POST the data you recieved from GET /api/v1/users/X/ to /api/v1/organizations/Y/admins/

Similarly, you can list admins of an organization if you are an org admin or superuser, with:

GET /api/v1/organizations/X/admins/

Note that adding a user as an admin does not automatically add them as a regular organization user.  If the user
is to be a member of any project teams, add them both to the admin list and the users list for a given organization.

Adding projects to an organization
----------------------------------

An organization may also have projects, which would be a concept like "ACME Corp Application" or "Application Foo".

Projects are covered in a later section, but are added to organizations, once created, by posting the record
recieved from /api/v1/projects/X/ to /api/v1/organizations/Y/.

Removing users, admins, and projects from organizations
-------------------------------------------------------

Deleting from sub-collections in Ansible Commander is not handled by a DELETE verb, but by a modified POST.

To remove a user ID X from an organization Y, simply POST the following to the collection /api/v1/organizations/Y/users/:

    { 'id' : X, 'disassociate' : 1 }

A similar post can also be made to /api/v1/organizations/Y/admins/ to remove an admin user or
/api/v1/organizations/Y/projects/.

The same removal facility is available elsewhere in Ansible commander for most related resources.

Projects
========

...

Teams
=====

...

Inventories
===========

...

Adding Inventories
------------------

Adding Hosts
------------

Adding Groups
-------------

Editing Hosts or Groups
-----------------------

Adding Host Variables
---------------------

Adding Group Variables
----------------------

Editing Host or Group Variables
-------------------------------

Removing Host or Group Variables
--------------------------------

Adding Sub Groups
-----------------

Removing Sub Groups
-------------------

Access Via Inventory Script
---------------------------

Credentials
===========

Creating credentials
--------------------

Adding credentials to users, teams, or projects
-----------------------------------------------

Seeing what credentials a user has access to
--------------------------------------------

Launch Jobs
===========

Submitting A Launch Job
-----------------------

Getting Job Results
-------------------

Browsing Log Data
-----------------


Tags
====

Adding Tags
-----------

Finding Tagged Resources
------------------------

Editing/Removing Tags
---------------------

Permissions
===========

Permissions can be granted to users or teams and indicate they are allowed to use
certain combinations of credentials, inventories to deploy to certain projects.

For instance, a permission may define that the QA Team can use certain credentials to push
to a Test Inventory, while another permission may indicate the Release Engineering team can
push a different project with different credentials to a Production inventory source.

Audit Trails
============

Viewing object audit trails
---------------------------

Additional Topics
=================

API Sorting And Filtering
-------------------------

Pagination Controls
-------------------

Alternative Content Types
-------------------------




