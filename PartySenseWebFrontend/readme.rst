Developer Documentation
=======================

For now all development has occurred on the domain partysense.hardbyte.webfactional.com


The api is in progress, these should work:

Event Setlist
--------------

    http://partysense.hardbyte.webfactional.com:8000/api/2/get-track-list

Will return all the tracks for event 2. No authentication is required.

Add track to setlist
--------------------

This will need authentifation and cross site tokens so won't work yet:

    POST
    {"name":"American Idiot","artist":"Green Day","spotifyTrackID":"spotify:track:6nTiIhLmQ3FWhvrGafw2zj"}

to the url:

    http://partysense.hardbyte.webfactional.com:8000/api/2/modify

To add the track "American Idiot" to event 2.

Vote on track
-------------

    POST {vote:false} or {vote:true} to the URL:
    http://partysense.hardbyte.webfactional.com:8000/api/2/vote/4/

Also requires authentication.

Remove track
------------

    POST to the URL:
    http://partysense.hardbyte.webfactional.com:8000/api/{event}/remove/{track}/

As the dj.