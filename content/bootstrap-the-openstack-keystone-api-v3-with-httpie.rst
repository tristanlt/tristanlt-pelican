Bootstrap the OpenStack Keystone API V3 with Httpie
###################################################
:date: 2015-04-05 14:01
:author: tristanlt
:tags: Cloud, OpenStack, Ubuntu
:slug: bootstrap-the-openstack-keystone-api-v3-with-httpie

|image0|\ Sometime, Openstack's clients are not compliant with latests
API versions. We should use Curl to create domains and openstack's
clients (python-keystoneclient or python-openstackclient) to manipulate
v2 identity objects. There is a way to simplify: exclusive use of Rest
API (with Curl for instance). However, curl is not design for humans...
Httpie was born from this fact, httpie simplifies commands by serialize
options to json and prettify results from commands. This post explains
how populate and use Openstack Keystone API V3 with Rest API with
httpie.

Well, when we bootstrap a fresh Keystone instance, we need :

-  An user which will become our cloud admin (1)
-  A project (2)
-  A role "admin" which is referenced in policy.json  (3)
-  | Grant admin role to our fresh user on our fresh project to
     become master of the world (Mouhouhahaha...)  (4)

   |Cloudadmin genesis|

| We need to grant admin role to our fresh user on your fresh project.
| We're starting from a fresh Openstack Keystone Juno installation on
  Ubuntu 14.04LTS (see : OpenStack Installation Guide for Ubuntu 14.04)

Httpie : Install and quickstart
===============================

Fortunately, Ubuntu repositories feeds httpie (version 0.8.0-1). We have
just to do :

::

    aptitude install httpie

Now, we can test **httpie** his **http** command line (replace URL by
your Keystone endpoint)

::

    root@32e2003091f8:/# http http://localhost:5000/v3

Then, read with relish pretty response :

::

    HTTP/1.1 200 OKContent-Length: 330Content-Type: application/jsonDate: Sat, 14 Mar 2015 12:46:03 GMTVary: X-Auth-TokenX-Distribution: Ubuntu{    "version": {        "id": "v3.0",         "links": [            {                "href": "http://localhost:5000/v3/",                 "rel": "self"            }        ],         "media-types": [            {                "base": "application/json",                 "type": "application/vnd.openstack.identity-v3+json"            },             {                "base": "application/xml",                 "type": "application/vnd.openstack.identity-v3+xml"            }        ],        "status": "stable",         "updated": "2013-03-06T00:00:00Z"    }}

If we're trying to request some restricted informations like users list,
we receive an error.

::

    http http://localhost:5000/v3/users

::

    ...{"error": {"message": "The request you have made requires authentication.", "code": 401, "title": "Unauthorized"}}...

We need to add  X-Auth-Token a header with our admin\_token. In order to
have shortest commands, we can place the endpoint adresse and the token
header in shell variables.

::

    export KV3="http://localhost:5000/v3/"export TOKADM="X-Auth-Token: ADMIN"http ${KV3}/users "${TOKADM}"

Now, we must have access to our API with admins privileges and receive
an empty user list.

::

    HTTP/1.1 200 OKContent-Length: 98Content-Type: application/jsonDate: Sat, 14 Mar 2015 13:18:32 GMTVary: X-Auth-TokenX-Distribution: Ubuntu{nbsp;   "links": {        "next": null,         "previous": null,         "self": "http://localhost:5000/v3/users"    },    "users": []}

What to do now
==============

We should add :

#. An user : cloudadmin
#. A project (ex-tenant) 
#. A role named "admin"
#. Grants this role to our brand new user on our brand new project

Add user clouadmin
==================

We have to make a POST request to our endpoint at URI /users. Httpie can
serialize some arguments but in our case we need to send nested json. At
this time, httpie doesn't work with nested data. We need tu use standard
input with echo or json file.

First we have to create a file which describes our admin user (names
user-cloudadmin.json)

::

    { "name": "cloudadmin", "email": "cloudadmin@ii.utav.fr", "password": "cloudadmin", "domain_id": "default"}

Next, we POST these data with user params (for nested json)

::

    http ${KV3}/users "${TOKADM}" user:=@user-cloudadmin.json

This command should answers

::

    ...{    "user": {        "domain_id": "default",         "email": "cloudadmin@ii.utav.fr",         "enabled": true,         "id": "1329df5966e84a1fae5728bbf828eca3",         "links": {            "self": "http://localhost:5000/v3/users/1329df5966e84a1fae5728bbf828eca3"        },         "name": "cloudadmin"    }}

Add project cloudadmin
======================

Next, we had to add a project. We create a file names
project-clouadmin.json

::

    {
        "name": "cloudadmin",
        "description": "Cloudadmin Projects",
        "domain_id": "default"
    }

Next, we POST this project into the Keystone v3 API with

::

     http ${KV3}/projects "${TOKADM}" project:=@project-cloudadmin.json

Keystone should answers something like

::

    {    "project": {        "description": "Cloudadmin Projects",         "domain_id": "default",         "enabled": true,         "id": "d2ae43e38e054b7fb8250ffe55a8d317",         "links": {            "self": "http://172.17.0.4:5000/v3/projects/d2ae43e38e054b7fb8250ffe55a8d317"        },        "name": "cloudadmin"    }}

Great! We have our user and our project.

Add role admin
==============

Now we must create a role, but not any role, THE role names "admin".
This role is referenced in /etc/keystone/policy.json has special. Any
user in any project become admin if it has this role. Roles are very
simple objects, we can use echo instead of a json file...

::

    echo '{ "role": { "name": "admin" } }' | http ${KV3}/roles "${TOKADM}"

Grant the role
==============

To grant a role to an user you must send a PUT request to :

**http://url-the-api/projects/**\ ${PROJECTID}\ **/users/**\ ${USERID}\ **/roles/**\ ${ROLEID}

In our case, we can search in our console history and create 3 shell
variables.

::

     export USERID="4dac9c47a778493490cf0c9467db9854" export PROJECTID="d2ae43e38e054b7fb8250ffe55a8d317" export ROLEID="f0fe064a794d405c82a8d58a6e652754"

Finally, send a PUT resquest to our endpoint.

::

     http PUT ${KV3}/projects/${PROJECTID}/users/${USERID}/roles/${ROLEID} "${TOKADM}"

PUT requests doesn't respond anything, that's fine.

Try our admin user
==================

Admin-Token in Keystone config file is definitively deprecated for
production. Our new user permit us to disable this configuration. To
test  our user we must : take a token for our user in our project
context, use this token to make a restricted operation on API (like list
users).

The Authentication API of Keystone is reachable at :
**http://\ **url-the-api**/auth/tokens**

We must POST json to this API on to retrieve a token. This json file is
like this one (named gettoken-cloudadmin.json)

::

    {   "auth": {    "identity": {        "methods": ["password"],        "password": {            "user": {                "name": "cloudadmin",                "domain": { "id": "default" },                "password": "cloudadmin"            }
            }    },    "scope": {        "project": {            "name": "cloudadmin",            "domain": { "id": "default" }        }    }  }}

And post this one in auth API with

::

    http -ph POST ${KV3}/auth/tokens < get-cloudadmin-token.json |grep X-Subject-Token

Note, the **-ph flag** (print only header) which make headers greppable.
Our token was return in header X-Subject-Token.

::

    X-Subject-Token: 231464f820134f1db088d77b333662dd

Finally, we can take copy this token into a new header and use this one
to authenticate our actions.

::

    export TOK="X-Auth-Token: 231464f820134f1db088d77b333662dd"
    http ${KV3}/users "${TOK}"
    HTTP/1.1 200 OK
    [...]

Job done, we have an admin user for our cloud... and a great tool to
manipulate objects...

.. |image0| image:: /img/openstack-logo5.png
   :width: 100px
   :height: 100px
.. |Cloudadmin genesis| image:: /img/keystone-bootstrap-superadmin-low.png
   :width: 600px
   :height: 154px
