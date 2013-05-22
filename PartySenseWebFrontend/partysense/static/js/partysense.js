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

function SpotifyCtrl($scope, $timeout, SpotifySearch, Track, updateService) {
    $scope.loggedIn = ps.loggedIn;

    $scope.doSearch = function() {
        if($scope.searchTerm.length > 2) {
            $scope.spotifyResult = SpotifySearch.get({q: $scope.searchTerm});
        }
    };

    $scope.clear = function(){
        $scope.spotifyResult = "";
        $scope.searchTerm = "";
        $scope.addTrackResult = false;
    };

    $scope.addTrack = function(track) {
        var newTrack = new Track({
                        "name": track.name,
                        "artist": track.artists[0].name,
                        "length": track.length,
                        "spotifyTrackID": track.href,
                        "spotifyArtistID": track.artists[0].href,
                        "external-ids": JSON.stringify(track["external-ids"])
                    });
        newTrack.$save(function(track, putResponseHeaders){
            console.log("sending event to update the set list");
            updateService.update("setlist");
            $scope.addTrackResult = true;
            $timeout(function() { $scope.addTrackResult = false; }, 2000);

        }, function(){
            $scope.addTrackResult = false;
        });
    };
}


function SetlistCtrl($scope, $http, Track, LastfmTrack, updateService) {

    $scope.infoWidth = ps.loggedIn ? 'span7' : 'span9';
    $scope.loggedIn = ps.loggedIn;
    $scope.spotifyPlaylistURL = "";

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

    $scope.$on("setlist", function(){
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
        newTrack.$save(function(track, putResponseHeaders){
            console.log("sending event to update the set list");
            updateService.update("setlist");
        });

        // Remove this track from the recentTracks list

        var i = ps.recentTracks.indexOf(track);
        if(i != -1) {
            ps.recentTracks.splice(i, 1);
        }
        $scope.recentTracks = ps.recentTracks;
    };
}