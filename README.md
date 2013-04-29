VDoc: Simple Document Versioning with Mongo and Django
======================================================

This is a simple project to provide an interface to a document store, where updates and additions both create new Mongo documents. Read operations bring back the most recent document by default.

Dependencies
------------

[Pymongo] (http://api.mongodb.org/python/current) v 2.5 (tested, earlier versions may work)

[Django 1.5] (https://www.djangoproject.com/)

[Bootstrap] (http://twitter.github.io/bootstrap/) and [JQuery] (http://jquery.com) are already in the static dir for the main app, and will be pulled in with a collectstatic.

The code assumes a MongoDB instance running on localhost without authentication.

Known Issues
------------

If a document update matches a previous version of the document, the update fails. This is due to the following code in insert_doc:

    db.update(doc, doc, upsert=True)

which does the versioning update atomically, but does not handle the aforementioned case.
