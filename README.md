
# Local Deployment
These steps get you a working PartySense server on your development machine. 

- Clone the repository (Use develop branch for beta site)
- Make sure you have python 2.7 installed along with pip
- In a terminal, in the *PartysenseWebFrontend* folder, execute
  `sudo pip install -r requirements.txt`
- Rename *possible_local_settings.py* to *local_settings.py*. The local settings will be used for deploying locally
- Next, run 3 commands on manage.py
	-  `python manage.py syncdb`
- Create a local admin if you plan to play with the Django Admin locally
	-  `python manage.py migrate`
- Once this is done, you should have a new file *development_database.db* in
  the webfrontend folder.
	-  `python manage.py runserver`
- You should now be able to see the partysense website on localhost:8000
- If you need to login with Facebook, you will need to add `127.0.0.1    partysen.se`
  to '/etc/hosts' file and visit *partysen.se:8000* in your browser instead. **Note**: The hosts file in windows can be found at `C:\\Windows\System32\drivers\etc\hosts`
- If you want to revert to viewing the live web version of the PartySense web app, you
  will need to comment the line added to hosts
- *Optional Step : Installing PostgreSQL* 
	.. tbd

# Server Deployment
Use these steps for deploying code on Hosted Server (possibly modified and tested on locally deployed version first)

SSH into `hardbyte@web388.webfaction.com`, should have ssh keys setup.

## Enable virtualenv

    workon pslive

    cd webapps/partysense/partysense

## version control update

    git pull

Or equivalently:

    git fetch
    git merge origin/master

## Update static files

    cd PartySenseWebFrontend
    python2.7 manage.py collectstatic

## If there were any schema changes

Read the south section!

## Trigger apache

    ~/webapps/partysense/apache2/bin/restart

## Switch back to using system python

    deactivate

It is possible to make changes on the server, but by default the SSH key
is configured for read only communication with bitbucket. So to push changes
on `master` from the server to bitbucket you would use your bitbucket user
account:

    git push https://{{username}}@bitbucket.org/tanmay_bhola/partysense.git master

# Hosting

The site is currently hosted on [webfaction][2]. The database is postgreSQL,
also hosted on webfaction, *[phpPgAdmin][3]* is a front end that can be used
to access the raw database.

> The database password can be found in the `settings.py` file.

# Server Technology

The server is split into three parts:

### Static Server

The heavy hitting **apache** serves all static files, this includes javascript,
images, custom css, and html fragments (templates).

The static server's contents are updated with:

    python2.7 manage.py collectstatic

### Django

The Python web development framework **Django** is our dynamic server. It is
the interface to our database. It encodes all the business logic of authentication,
creating and editing events, voting on setlists etc.

### Memcached

[memcached][5] works as a (fast) map of some unique ID -> content.
For example on the event page, the following caches all the track information:

    {% cache 600 eventdata event.pk request.user.pk %}

Memcached itself is started with:

    memcached -d -m 64 -s $HOME/memcached.sock -P $HOME/memcached.pid

To stop memchached use:

    kill $(cat $HOME/memcached.pid)


Two django applications that are used for partysense are `python-social-auth`
for logging in with facebook, and `django-compressor` for minifying css and
javascript files on the fly.

## Client

Most of the smarts of the website are *client side*. For instance our database only
keeps small amounts of data about particular **Tracks**, the client requests further
information from both **Spotify** and **Last.fm**. To achieve this our javascript
stack includes:

- AngularJS
- Bootstrap3
- JQuery

We also load things like Google Maps, Google Places, and D3 when required.

# Testing Procedure

As a minimum before pushing a change run the site locally with:

    python manage.py runserver

And make sure you can see the main page, the profile page and the event page.

On the event page make sure you can search for tracks, add a track, and vote
on a track. Create a new event - it doesn't take too long.

Python dependencies are all listed in `requirements.txt`. All the javascript
dependencies are in the `static/lib` folder.

## Versions

django 1.5.4 and python 2.7.

Upgrading docs: http://docs.webfaction.com/software/django/config.html#upgrading-your-django-libraries

# API

## v1 tastypie api

Used to list club details, locations and users.

[Tastypie tutorial](http://django-tastypie.readthedocs.org/en/latest/tutorial.html)

## Old event api

This **api** is used by the [partysen.se][1] website, so these commands are pretty well tested:

## Get an Event's Setlist

    /api/{event id}/get-track-list

**No authentication required**.

For example the URL [http://partysen.se/api/2/get-track-list][4] will return
all the tracks as JSON for event 2.

	[{"spotifyTrackID": "spotify:track:1mwt9hzaH7idmC5UCoOUkz", "upVotes": 4, "name": "Diamonds", "removable": false, "artist": "Rihanna", "pk": 20, "downVotes": 0, "usersVote": null}, {"spotifyTrackID": "spotify:track:3bbUkaQYGQHkx1TJi7gPSL", "upVotes": 4, "name": "Kryptonite", "removable": false, "artist": "3 Doors Down", "pk": 8, "downVotes": 0, "usersVote": null}, {"spotifyTrackID": "spotify:track:45T1EKlWGKFfiE0iIVfb04", "upVotes": 6, "name": "Thunderstruck", "removable": false, "artist": "AC/DC Tribute Band", "pk": 3, "downVotes": 2, "usersVote": null}, ...


## Adding a track to an event's Setlist

POST to the url `/api/{event}/modify/`:

    {
        "name":"American Idiot",
        "artist":"Green Day",
        "spotifyTrackID":"spotify:track:6nTiIhLmQ3FWhvrGafw2zj"
    }

This api call requires the user to be logged in. This request will add the user to
the event if they don't already belong. This will automatically add an up vote from
the user.

## Vote on track

POST `{vote:false}` or `{vote:true}` to the URL:

    /api/{event}/vote/{track}/

This api call requires the user to be logged in. This request will add the user to
the event if they don't already belong.

## Remove track from event

As a logged in user `POST` to the URL:

    /api/{event}/remove/{track}/

The track will be removed **if** the user is the DJ for that event,
or (TODO) if there were no up votes.

## Amazon Product Query

To get an amazon product URL

    GET {artist: "", track: ""} to
    /amazon/purchase/

Response will be a JSON object containing:

    'ASIN', 'URL', 'image', 'price'


# Misc

## Virtualenv

I've set up the server to use virtualenv based of this [blog][6].


## South

South is a database migration tool that we should be using.

Start with a new schema migration per app:

    ./manage.py migrate myapp 0001 --fake

on every machine that has a copy of the codebase (make sure they were up-to-date with
models and schema first).

Then when the schema changes (new fields etc) make a migration:

    ./manage.py schemamigration event --auto

This will create a migration in `event/migrations/0002_auto__description`. Look at the generated code
and write forwards and backwards migrations.

To apply the migration run:

    ./manage.py migrate event

## Amazon API

The server contains a `~/.amazon-product-api` file with:

    [Credentials]
    access_key = AKIAJ6HNZC6HWILISCKA
    secret_key = 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
    associate_tag = 6404-2547-9415


[1]: http://partysen.se
[2]: http://webfaction.com/
[3]: https://web388.webfaction.com/static/phpPgAdmin/
[4]: http://partysen.se/api/2/get-track-list
[5]: http://docs.webfaction.com/software/memcached.html
[6]: http://theneum.com/blog/webfaction-virtualenv-how-to/