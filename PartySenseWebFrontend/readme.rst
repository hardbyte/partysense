Developer Documentation
=======================

During development I've used the domain partysense.hardbyte.webfactional.com

Database
========

I'm using postgres2 because that should be good for production as well as development.

Deployment for now while I don't have south
- Drop tables that have changed.
- ssh into server and run python2.7 manage.py syncdb
- python2.7 manage.py collectstatic

TODO:
    - Implement Reviews!
    - style
