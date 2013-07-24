var App = angular.module('Partysense',
  ['ngResource', 
   'ps.filters', 
  'ps.services']);

App.directive('backImg', function(){
    return function(scope, element, attrs){
        attrs.$observe('backImg', function(value) {
            element.css({
                'background-image': 'url(' + value +')',
                //'background-size' : 'cover',
                'background-position' : 'right',
                'background-repeat' : 'no-repeat'
            });
        });
    };
});

App.directive('droppable', function($compile, $rootScope, updateService) {
    "use strict";
    return {
        restrict: "A",
        //The link function is responsible for registering DOM listeners as well as updating the DOM.
        link: function(scope, element, attrs){

            element.context.ondragover = function(event) {
                // TODO maybe we can work out if this is from spotify here?
                if(true){
                    // Do something to show we can deal with items dropped on this
                    element.addClass("indicate-drop");
                    return false;
                } else {
                    console.log("I don't know how to deal with that... should I?");
                    console.log(event);
                }
            };

            element.context.ondragleave = function(event){
                attrs.$set('class', '');
            };

            element.context.ondrop = function (event) {
                // work out if this is something we can deal with...
                // get an open url:
                //http://open.spotify.com/user/1242959390/playlist/4rN0f6C22Mz9dUX5lcbG5F
                var open_url = event.dataTransfer.getData("text/plain");
                console.log(open_url);
                if(/.*spotify.*/.test(open_url)){

                    var uri = event.dataTransfer.getData("text/uri-list");
                    //spotify:user:1242959390:playlist:4rN0f6C22Mz9dUX5lcbG5F

                    //console.log(event.dataTransfer.getData("text/html"));
                    // <a href="http://open.spotify.com/user/1242959390/playlist/4rN0f6C22Mz9dUX5lcbG5F">Trial</a>

                    var el = document.createElement( 'div' );
                    el.innerHTML = event.dataTransfer.getData("text/html");
                    var name = el.innerText;

                    var type = "";
                    
                    if(/spotify[:].*playlist:.*/g.test(uri)){
                        console.log("Looks like " + uri + " is a playlist");
                        type = "playlist - I can't import that from spotify sorry";
                    } 
                    if(/spotify[:].*album:.*/g.test(uri)) {
                        type = "album";
                        $rootScope.$apply(function(){
                            updateService.update("importAlbumBySpotifyURI", uri);
                        });
                    }
                    if(/spotify[:].*artist:.*/.test(uri)) {
                        //console.log("Looks like " + uri + " is an artist");
                        type = "artist";
                        /* The html already has the artist name, so lets just use that... (is that a hack?)*/
                        
                        var artist = {name: name, href: uri};
                        // IMPORTANT to call $apply to force AngularJS to notice that we change stuff!
                        $rootScope.$apply(function(){
                            updateService.update("searchByArtist", artist);
                        });
                        
                    }
                    if(/spotify[:].*track:.*/.test(uri)) {
                        console.log("Looks like " + uri + " is a track");
                        type = "track";
                        $rootScope.$apply(function(){
                            updateService.update("addTrackBySpotifyURI", uri);
                        });
                    }

                    // Send a message letting the user know what we are doing
                    $rootScope.$apply(function(){
                        updateService.update("showMsg",
                            "Importing Spotify " + type + " - " + name + ".");
                    });

                    // Seems if I don't preventDefault then spotify will start playing...
                    event.preventDefault();

                    // Remove the extra class we added to show this accepts dropping stuff
                    attrs.$set('class', '');
                    //return false;
                }
            };
        }
    };
});

/* Template Controller will pull in all the other HTML fragments
 * and the other Angular Controllers */
function TemplateCtrl($scope) {
    "use strict";
    $scope.oneAtATime = true;
    $scope.loggedIn = ps.loggedIn;
    $scope.resultListTemplate = "/static/spotifyResultList.html";
    $scope.previewTemplate = "/static/spotifyPreview.html";
    $scope.setlistTemplate = "/static/eventsTrackList.html";
    $scope.recentTracksTemplate = "/static/recentTrackList.html";
    $scope.eventStatisticsTemplate = "/static/eventStatistics.html";
}

function EventStatsCtrl($scope, Track, updateService){
    "use strict";

    $scope.refreshTracks = function(){
        // GET: /api/123/get-track-list
        $scope.setlist = Track.query({action: "get-track-list"}, function(data){
            console.log("Received setlist");
            var artists = [];

            // TODO - consider doing this server side!
            data.forEach(function(track){
                console.log(track.artist);
                track.votes = track.upVotes - track.downVotes;
                // Is this artist in our list?
                if(!artists.some(function(a, i, artists){
                    var res = a.name === track.artist;
                    if(res){
                        // Seen it before add the votes
                        artists[i].votes += track.votes;
                        if(track.votes > 0){
                            artists[i].numberOfTracks++;
                        }
                    }
                    return res;
                })){
                    // no -> add it
                    var a = {name: track.artist};
                    a.votes = track.votes;
                    // Only record the track if its got a positive rank
                    if(a.votes > 0){
                        a.numberOfTracks = 1;
                    } else {
                        a.numberOfTracks = 0;
                    }
                    artists.push(a);
                }
            });

            $scope.mostPopularArtists = artists.sort(function(a, b){
                return b.votes - a.votes;
            }).slice(0, Math.min(5, artists.length));

            $scope.artistsWithMostTracks = artists.sort(function(a, b){
                return b.numberOfTracks - a.numberOfTracks;
            }).slice(0, Math.min(5, artists.length));


            $scope.popularTracks = data.sort(function(b, a){
                return (a.upVotes - a.downVotes) - (b.upVotes - b.downVotes);
            }).slice(0, Math.min(5, data.length));


        });
    };

    $scope.refreshTracks();
}

function SpotifyCtrl($scope, $timeout, $http, SpotifySearch, SpotifyLookup, Track, updateService) {
    "use strict";

    function filterResults(data) {
        // If there aren't many tracks don't bother scrolling
        if($scope.spotifyResult.tracks) {
            $scope.scrollableClass = $scope.spotifyResult.tracks.length > 10 ? "pre-scrollable" : "";
            $scope.msg = "";
        }
        if($scope.spotifyResult.info.num_results == 0) {
            $scope.msg = "Sorry no results";
        }
        /* Scroll up to the search box to show the new results. */
        document.getElementById("search").scrollIntoView(false);
    }

    $scope.msg = "";
    $scope.loggedIn = ps.loggedIn;

    $scope.doSearch = function(force, append, skipSpellCheck) {
        console.log("doSearch called");
        console.log($scope.searchTerm);
        $scope.correction = "";

        if($scope.searchTerm.length === 0){
            $scope.clear();
        }

        if($scope.searchTerm.length > 3 || force) {
            $scope.msg = 'searching for "' + $scope.searchTerm + '"';
            console.log($scope.msg);
            if (!skipSpellCheck) {
                // Send the search term to our server to query google
                $http.get("/did-you-mean?q=" + $scope.searchTerm).success(function(data) {
                    if(data.changed && data.changed !== $scope.searchTerm ) {
                        $scope.correction = data.changed;
                    }
                });
            }
            if(append){
                SpotifySearch.get({q: $scope.searchTerm}, function(data){
                    console.log("Adding " + data.tracks.length + " new tracks to existing results");
                    $scope.spotifyResult.tracks = $scope.spotifyResult.tracks.concat(data.tracks);
                    filterResults();
                });
            } else {
                console.log("Conducting new search for query:"  + $scope.searchTerm );
                $scope.spotifyResult = SpotifySearch.get({q: $scope.searchTerm}, filterResults);
            }
        }
    };

    $scope.clear = function(){
        console.log("Clearing search");
        $scope.spotifyResult = false;
        $scope.searchTerm = "";
        $scope.addTrackResult = false;
        $scope.msg = "";
        $scope.correction = "";
    };

    $scope.searchArtist = function(artist){
        console.log("It appears you want to search for an artist:");
        console.log(artist.name);
        // replace the search with this artist's name
        $scope.searchTerm = "artist:" + artist.name;

        // Filter the existing tracks for this artist (if there ary any results)
        if($scope.spotifyResult) {
            console.log("Since we already have search results, filter for this artist");
            console.log("Looking for matches to " + artist.href);

            var filtered_tracks = $scope.spotifyResult.tracks.filter(function(track){
                return track.artists[0].href === artist.href;
            });
            console.log("Found " + filtered_tracks.length + " tracks.");
            $scope.spotifyResult.tracks = filtered_tracks;
        } else {
            console.log("There were no prior results so just search");
            return $scope.doSearch(true, false, true);
        }
        // Note the number of results shown may be less than this due to filtering
        if ($scope.spotifyResult.tracks.length > 15) {
            // If there aren't many tracks don't bother scrolling
            $scope.scrollableClass = "pre-scrollable";
        } else {
            console.log("There weren't enough tracks by this artist so conducting another search");

            // search for tracks by this artist
            $scope.doSearch(true, true, false);
        }

    };

    $scope.$on("searchByArtist", function(evt, artist){
        console.log("Searching for tracks by");
        console.log(artist);
        $scope.searchArtist(artist);
    });

    $scope.$on("showMsg", function(evt, msg){
        console.log("received a showMsg event");
        $scope.msg = msg;
        $scope.msgClass = "alert-success";
    });

    $scope.$on("addTrackBySpotifyURI", function(evt, uri){
        SpotifyLookup.get({uri: uri}, function(data){
            console.log("heard back from spotify for " + uri);
            $scope.addTrack(data.track);
        });
    });

    $scope.$on("importAlbumBySpotifyURI", function(evt, uri){
        SpotifyLookup.get({uri: uri, extras: "trackdetail"}, function(data){
            console.log("heard back from spotify for " + uri);
            console.log(data);
            data.info.num_results = 1;
            $scope.spotifyResult = {info: data.info, tracks: data.album.tracks};
            filterResults();
        });
    });

    $scope.addTrack = function(track) {
        console.log("Adding track");
        var newTrack = new Track({
                        "name": track.name,
                        "artist": track.artists[0].name,
                        "length": track.length,
                        "spotifyTrackID": track.href,
                        "spotifyArtistID": track.artists[0].href,
                        "external-ids": JSON.stringify(track["external-ids"])
                    });
        newTrack.$save(function(t, putResponseHeaders){
            updateService.update("setlist");
            $scope.addTrackResult = true;
            $scope.msg = "Added " + track.name + " to the setlist!";
            $scope.msgClass = "alert-success";
            track.added = true;
            $timeout(function() { $scope.msg = ""; }, 5000);
        }, function(){
            console.log("failure to add track");
            $scope.msgClass = "alert-error";
            track.msg = "Opps, something went wrong adding " + track.name;
            $timeout(function() { $scope.msg = ""; }, 5000);
        });
    };
}


function SetlistCtrl($scope, $http, Track, LastfmTrack, updateService) {
    "use strict";
    $scope.infoWidth = ps.loggedIn ? 'span7' : 'span9';
    $scope.loggedIn = ps.loggedIn;
    $scope.spotifyPlaylistURL = "";
    $scope.numberOfTracks = ps.numberOfTracks;

    $scope.searchArtistFromTrack = function(track) {
        console.log("want to search for an artist do you?");
        console.log(track);
        var artist = {
            name: track.artist,
            href: track.spotifyArtistID
        };
        updateService.update("searchByArtist", artist);
    };

    $scope.updateSetlist = function(){
        // GET: /api/123/get-track-list
        $scope.setlist = Track.query({action: "get-track-list"}, function(data){
            var songs = "";
            var i;
            for(i=0; i<data.length; i++){
                findCover(data[i]);
                songs += data[i].spotifyTrackID.slice(14) + ',';
            }
            $scope.playlistSongs = songs;
            $scope.spotifyPlaylistURL = "http://embed.spotify.com/?uri=spotify:trackset:" + $scope.playlistName + ":" + $scope.playlistSongs + "&view=list";
        });
    };

    $scope.updateSetlist();

    $scope.$on("setlist", function(evt, track){
        console.log("It appears you're adding a track to the setlist");
        console.log(track);
        // TODO really we could do this smarter...
        $scope.updateSetlist();
    });

    // encode the events name in the spotify playlist
    $scope.playlistName = encodeURIComponent("Partysense - " + ps.eventTitle);

    $scope.removeTrack = function(track) {
        $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
        $http.post("/api/" + ps.event + "/remove/" + track.pk + "/").success(
          function(response){
            console.log(response);
            $scope.updateSetlist();
          });
    };

    $scope.vote = function (track, isUpVote) {
        console.log("Got a vote!");
        console.log(track);
        // TODO replace with $resource
        /* Protection against cross site scripting attacks. */
        $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
        $http.post("/api/" + ps.event + "/vote/" + track.pk + "/",
          {vote: isUpVote}).success(function(response){
            track.usersVote = isUpVote;
            if(response.created) {
                if(isUpVote){
                    track.upVotes += 1;
                } else {
                    track.downVotes += 1;
                }
            }
        });

    };

 /*
    If lastfm cannot find the song the response will be:
    {error: 6, message: "track not found"}

    Otherwise the data.track **might** have all of the following fields:
        mbid
        duration
        toptags -> tags -> [0, ..., 4] -> {name: "indie"}
        album -> image -> [smallest, ..., largest] -> {#text: image url, size}
                 mbid
                 artist
        artist -> mbid
                  name
                  url
        wiki
*/
    function findCover(track){
        var updateCover = function(data){
            if(data.hasOwnProperty("track") && data.track.hasOwnProperty("album")){
                var albumImages = data.track.album.image;
                // Select the largest one...
                //track.coverURL = albumImages[albumImages.length - 1]['#text'];
                // The "medium" sized image
                track.coverURL = albumImages[1]['#text'];
            }
            if(data.hasOwnProperty("track") &&
               data.track.hasOwnProperty("toptags") &&
               data.track.toptags.hasOwnProperty("tag")) {
                if(Array.isArray(data.track.toptags.tag)) {
                    track.tag = data.track.toptags.tag[0].name;
                } else {
                    // could just be a string "pop rap"
                    track.tag = data.track.toptags.tag.name.split(" ")[0];
                }
            }
        };

        var cacheCover = function(track, data) {
            localStorage[track.spotifyTrackID] = JSON.stringify(data);
        };
        // See if we have localStorage and if this track has been stored
        if(supports_html5_storage() && track.spotifyTrackID in localStorage) {
            updateCover(JSON.parse(localStorage[track.spotifyTrackID]));
            return;
        }
        // Otherwise we need to query lastfm about this track
        LastfmTrack.get({track: track.name, artist: track.artist},
          function(data) {
              if(supports_html5_storage()) {
                  cacheCover(track, data);
              }
              updateCover(data);
          });
    }
}

function RecentTrackCtrl($scope, Track, updateService) {
    $scope.recentTracks = ps.recentTracks;
    $scope.loggedIn = ps.loggedIn;
    $scope.addTrack = function(track) {
        console.log("Adding previously used track");
        console.log(track);

        // GET Track from db, then POST to this event?
        var newTrack = new Track({
                        "name": track.name,
                        "artist": track.artist,
                        "spotifyTrackID": track.spotify_url
                    });
        newTrack.$save(function(t, putResponseHeaders){
            console.log("sending event to update the set list");
            updateService.update("setlist", track);
        });

        // Remove this track from the recentTracks list

        var i = ps.recentTracks.indexOf(track);
        if(i != -1) {
            ps.recentTracks.splice(i, 1);
        }
        $scope.recentTracks = ps.recentTracks;
    };
}