Developer Documentation
=======================

> partysen.se


The api is in progress, these should work:

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

Note only the dj currently has permission to do this.

TODO
----

Angular directive for <track upVotes="3" downVotes="0 ...>

