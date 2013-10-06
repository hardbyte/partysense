Developer Documentation
=======================

> partysen.se

Repository Structure
---------------------

**PartySenseApp** : Code for the android application
**PartySenseAppiOS** : Code for the iOS application
**PartySenseWebBackend**: Google App Engine Server for partysenseapp.appspot.com
**PartySenseWebFrontend**: Complete Web Application including the partysen.se website

Local Deployment
----------------

- Clone the repository (Use develop branch for beta site)
- Make sure you have python 2.7 installed along with Pip
- In a terminal, in the PartysenseWebFrontend folder, execute `sudo pip install -r requirements.txt`
- Next, run `python manage.py syncdb` . If this gives *DatabaseError: no such table: music_idtype*, temporarily comment the line `_spotify_type = IDType.objects.get(pk=1)`  from music\models.py
- Once this is done, you should have a new file *development_database.db* in the webfrontend folder
- Run `python manage.py runserver`
- You only need to create a local admin if you need to play with the Django Admin locally
- You should now be able to see the partysense website on *localhost:8000*
- If you need to login with Facebook, you will need to add `127.0.0.1    partysen.se` to '/etc/hosts' file and visit *partysen.se:8000* in your browser instead
      - Note: The hosts file in windows can be found at 'C:\\Windows\System32\drivers\etc\hosts'
- If you want to revert to visiting the web version of the PartySense web app, you will need to comment the line added to hosts.


Testing Procedure
-----------------

As a minimum before pushing a change run the site locally with:

    python manage.py runserver

And make sure you can see the main page, the profile page and the event page.

On the event page make sure you can search for tracks, add a track, and vote on a track.
Ideally we would also create a new event but that takes too long.


Python dependencies are all listed in requirements.txt. All the javascript dependencies
are in the static/lib folder. At the moment I'm using django 1.5 and python 2.7. I'd
like to switch to python3, which is installed on the server...


API
===

While the restfull api is in progress, these should work:

Event Setlist
--------------

    /api/2/get-track-list

Will return all the tracks for event 2. No authentication is required.

Add track to setlist
--------------------

This will need authentication and cross site tokens so won't work yet:

    POST
    {"name":"American Idiot","artist":"Green Day","spotifyTrackID":"spotify:track:6nTiIhLmQ3FWhvrGafw2zj"}

to the url:

    /api/2/modify

To add the track "American Idiot" to event 2.

Vote on track
-------------

    POST {vote:false} or {vote:true} to the URL:
    /api/2/vote/4/

Also requires authentication.

Remove track
------------

    POST to the URL:
    /api/{event}/remove/{track}/

As the dj.


=========
Memcached
=========

Works as a map of some unique ID to some content.
For example on the event page, the following caches all the track information:

    {% cache 600 eventdata event.pk request.user.pk %}

Memcached itself is started with:

    memcached -d -m 64 -s $HOME/memcached.sock -P $HOME/memcached.pid

=====
South
=====

South is a database migration tool.

Start with a new schema migration per app:

    ./manage.py convert_to_south event

The convert_to_south command only works entirely on the first machine you run it on.
Once you’ve committed the initial migrations it made into your VCS, you’ll have to run

    ./manage.py migrate myapp 0001 --fake

on every machine that has a copy of the codebase (make sure they were up-to-date with
models and schema first).


Then when the schema changes (new fields etc) make a migration:

    ./manage.py schemamigration event --auto


Deployment Steps
----------------

SSH into hardbyte@web388.webfaction.com

cd webapps/partysense_beta

1) version control update

    git pull

2) Update static files

    python2.7 manage.py collectstatic

3) Trigger apache

    touch wsgi.py