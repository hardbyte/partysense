Party Sense Sync
================

A Python application for scanning a hosts music collection and pointing out
what music they have and don't have for a particular event.

Primary flow
------------

We need to achieve two things:

1) Need to get information from the user about which event they are trying to
   get the music from. Options for this include having the user get a token from
   the partysen.se website (to be determined how). Or the user might have to
   login to this application (authenticate with ps/fb) and then select from their
   events.

   The app does a GET request to fetch all of the track info. This includes
   all the votes.

2) Need to get information from the user about where they store their music.
   Expect to have to handle multiple directories, and being DJs these directories
   could have extremely large quantities of music.
   The app then analyses these directories and makes a database of all the music found.
   In theory we might be able to hook into Windows Media Player and/or iTunes Library
   and just query their database? TODO: determine if that is plausible?

   Ideally we can handle a few hundred GB in less than half an hour (ideally much quicker).

With these two pieces of information the app then processes what tracks are missing
and what tracks are already there. Giving nice intuitive options like "Buy Missing Tracks",
"Create iTunes playlist", "Export tracks to folder", "Play tracks with ..."

I wonder how many djs would like a "Start downloading missing tracks from the Pirate Bay"
option. :-P


Technology
----------

Haven't decided whether to use Python or Java. There are benefits of each.

Python
~~~~~~

If we decide to implement in Python:

* py2exe or some method of turning the app into a .exe will be required.

* A library called watchdog might be useful in later versions for getting notified
  when music has been added to the filesystem. https://github.com/gorakhargosh/watchdog