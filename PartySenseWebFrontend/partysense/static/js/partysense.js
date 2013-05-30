angular.module('Partysense', ['ngResource', 'ps.filters', 'ps.services']);

/* Templating Controllers */
function SpotifyTemplateCtrl($scope) {
    $scope.template = "/static/spotifyResultList.html";
}

function PreviewTemplateCtrl($scope) {
    $scope.template = "/static/spotifyPreview.html";
}

function SetlistTemplateCtrl($scope) {
    $scope.template = "/static/eventsTrackList.html";
}

function RecentTracksTemplateCtrl($scope) {
    $scope.template = "/static/recentTrackList.html";
}



function SpotifyCtrl($scope, $timeout, $http, SpotifySearch, Track, updateService) {
    "use strict";

    function filterResults(data){
        // If there aren't many tracks don't bother scrolling
        if($scope.spotifyResult.tracks) {
            $scope.scrollableClass = $scope.spotifyResult.tracks.length > 10 ? "pre-scrollable" : "";

            // If the track has the same artist, the name can't be too similar?
            // Artists like Mumford & Sons release "Little Lion Man" on multiple
            // albums and Spotify has seperate instances of those tracks.
            // The external ids and the names match though.
            // Also want to ensure we keep one of them!
            $scope.spotifyResult.tracks = $scope.spotifyResult.tracks.filter(function(track, i, array){
                return !array.some(function(innerTrack, j){
                    return i > j && i != j && track.name === innerTrack.name;
                });
            });
        }
        /* Scroll up to the search box to show the new results. */
        document.getElementById("search").scrollIntoView(false);
    }
    $scope.msg = "";
    $scope.loggedIn = ps.loggedIn;

    $scope.doSearch = function(force, append) {
        $scope.msg = "";
        $scope.correction = "";

        if($scope.searchTerm.length > 3 || force) {
            // TODO only do this spelling check if the user has paused
            // Send the search term to our server to query google
            $http.get("/did-you-mean?q=" + $scope.searchTerm).success(function(data) {
                if(data.changed) {
                    $scope.correction = data.changed;

                    /*
                    $scope.searchTerm = data.changed;
                    $scope.doSearch(true);
                    */
                } else {
                    $scope.msg = "";
                }
            });

            if(append) {
                SpotifySearch.get({q: $scope.searchTerm}, function(data){
                    console.log("Adding new tracks");
                    $scope.spotifyResult.tracks = $scope.spotifyResult.tracks.concat(data.tracks);
                    filterResults();
                });
            } else {
                $scope.spotifyResult = SpotifySearch.get({q: $scope.searchTerm}, filterResults);
            }

        }
    };

    $scope.clear = function(){
        $scope.spotifyResult = "";
        $scope.searchTerm = "";
        $scope.addTrackResult = false;
        $scope.msg = "";
    };

    $scope.searchArtist = function(artist){
        console.log("It appears you want to search for an artist:");
        console.log(artist.name);
        // replace the search with this artist's name
        $scope.searchTerm = "artist:" + artist.name;

        // Filter the existing tracks for this artist (if there ary any results)
        if($scope.spotifyResult) {
            $scope.spotifyResult.tracks = $scope.spotifyResult.tracks.filter(function(track){
                "use strict";
                return track.artists[0].href === artist.href;
            });
        } else {
            /* There were no results so just search */
            return $scope.doSearch(true);
        }

        if ($scope.spotifyResult.tracks.length > 10) {
            // If there aren't many tracks don't bother scrolling
            $scope.scrollableClass = "pre-scrollable";
        } else {
            // If there weren't enough (>10) conduct another search
            // search for tracks by this artist
            $scope.doSearch(true, true);
        }

    };

    $scope.$on("searchByArtistName", function(evt, artist){
        console.log("Searching for tracks by");
        console.log(artist);
        $scope.searchArtist(artist);
    });
    $scope.addTrack = function(track) {
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
            // failure case
            $scope.msgClass = "alert-error";
            track.msg = "Opps, something went wrong adding " + track.name;
            $timeout(function() { $scope.msg = ""; }, 5000);
        });
    };
}


function SetlistCtrl($scope, $http, Track, LastfmTrack, updateService) {

    $scope.infoWidth = ps.loggedIn ? 'span7' : 'span9';
    $scope.loggedIn = ps.loggedIn;
    $scope.spotifyPlaylistURL = "";

    $scope.searchByArtist = function(track) {
        "use strict";
        console.log("want to search for an artist do you?");
        console.log(track);
        var artist = {
            name: track.artist,
            href: track.spotifyArtistID
        };
        updateService.update("searchByArtistName", artist);
    };
    $scope.updateSetlist = function(){
        // GET: /api/123/get-track-list
        $scope.setlist = Track.query({action: "get-track-list"}, function(data){
            var songs = "";
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
        console.log("It appears you're adding a track");
        console.log(track);
        $scope.updateSetlist();
    });

    // encode the events name in the spotify playlist
    $scope.playlistName = encodeURIComponent("Partysense - " + ps.eventTitle);

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