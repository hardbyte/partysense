var App = angular.module('Partysense',
  ['ngResource', 
   'ps.filters', 
   'ps.services',
   'ps.directives']);

/* Template Controller will pull in all the other HTML fragments
 * and the other Angular Controllers */
function TemplateCtrl($scope) {
    "use strict";
    $scope.oneAtATime = true;
    $scope.loggedIn = ps.loggedIn;
    $scope.resultListTemplate = "/static/partials/searchResults.html";
    $scope.previewTemplate = "/static/partials/spotifyPreview.html";
    $scope.setlistTemplate = "/static/partials/eventsTrackList.html";
    $scope.recentTracksTemplate = "/static/partials/recentTrackList.html";
    $scope.eventStatisticsTemplate = "/static/partials/eventStatistics.html";
}

function EventStatsCtrl($scope, Track, updateService){
    "use strict";
    $scope.setlist = ps.setlist;

    $scope.refreshTracks = function(){
        // GET: /api/123/get-track-list
        //$scope.setlist = Track.query({action: "get-track-list"}, function(data){

        var data = ps.setlist;

            $scope.numberOfResults = Math.min(10, $scope.setlist.length);
            var artists = [];

            // TODO - consider doing this server side!
            data.forEach(function(track){
                track.votes = track.upVotes - track.downVotes;
                // Is this tracks' artist in our list?
                if(!artists.some(function(a, i, artists){
                    var res = a.name === track.artist;
                    if(res){
                        // Seen this artist before so add the votes
                        artists[i].votes += track.votes;
                        if(track.votes > 0){
                            artists[i].numberOfTracks++;
                        }
                    }
                    return res;
                })){
                    // no -> add it
                    var a = {name: track.artist, votes: track.votes};

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
            }).slice();

            $scope.artistsWithMostTracks = artists.sort(function(a, b){
                return b.numberOfTracks - a.numberOfTracks;
            }).slice();


            $scope.popularTracks = data.sort(function(b, a){
                return (a.upVotes - a.downVotes) - (b.upVotes - b.downVotes);
            });
        //});
    };

    $scope.refreshTracks();
}

function SearchCtrl($scope, $timeout, $http, SpotifySearch, SpotifyLookup, Track, updateService) {
    /* This is really the search controller (currently spotify) */
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

    function refreshSetlist(data){
        var songs = "";
        var i;
        for (var j = 0; j < data.length; j++) {
            data[j].coverURL = "/static/images/defaultCover.png";
            findCover(data[j]);
        }

        for(i=0; i<Math.min(80, data.length);i++){
            songs += data[i].spotifyTrackID.slice(14) + ',';
        }
        $scope.playlistSongs = songs;
        $scope.spotifyPlaylistURL = "http://embed.spotify.com/?uri=spotify:trackset:" + $scope.playlistName + ":" + $scope.playlistSongs + "&view=list";
        return data;
    }

    $scope.updateSetlist = function(){
        // GET: /api/123/get-track-list
        $scope.setlist = Track.query({action: "get-track-list"}, refreshSetlist);
    };

    //$scope.updateSetlist();
    $scope.setlist = refreshSetlist(ps.setlist);

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
        // and genre
        var updateCover = function(data){
            if(data.hasOwnProperty("track") && data.track.hasOwnProperty("album")){
                var albumImages = data.track.album.image;
                // Select the cover from what last.fm provides
                // Largest:
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