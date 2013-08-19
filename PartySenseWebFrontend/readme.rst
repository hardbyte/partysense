Developer Documentation
=======================

> partysen.se


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