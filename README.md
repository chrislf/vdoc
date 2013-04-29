VDoc: Simple Document Versioning with Mongo and Django
======================================================

This is a simple project to provide an interface to a document store, where updates and additions both create new Mongo documents. Read operations bring back the most recent document by default.

Dependencies
------------

[Pymongo] (http://api.mongodb.org/python/current) v 2.5 (tested, earlier versions may work)
<<<<<<< HEAD

[Django 1.5] (https://www.djangoproject.com/)

=======
[Django 1.5] (https://www.djangoproject.com/)

>>>>>>> 02ae0baf0e4bfdc49739fe093babcc1fd894d63d
[Bootstrap] (http://twitter.github.io/bootstrap/) and [JQuery] (http://jquery.com) are already in the static dir for the main app, and will be pulled in with a collectstatic.

The code assumes a MongoDB instance running on localhost without authentication.
