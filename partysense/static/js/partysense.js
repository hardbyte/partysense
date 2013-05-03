angular.module('Partysense', ['ngResource']);

function SpotifyTemplateCtrl($scope) {
    $scope.template = "/static/spotifyResultList.html";
}

function SpotifyCtrl($scope, $http, $resource) {
    /* Protection against cross site scripting attacks. */
    $http.defaults.headers.post['X-CSRFToken'] = csrftoken;

    /* Resources */
    $scope.spotify = $resource("http://ws.spotify.com/search/1/:action",
      {action: 'track.json', q:'Gaga'}
    );

    var Track = $resource("/api/:event/modify",
      {event: ps.event}
    );

    $scope.doSearch = function() {
        $scope.spotifyResult = $scope.spotify.get({q: $scope.searchTerm});
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
            updateTrackView();
        });
    };
}

function SetlistTemplateCtrl($scope) {
    $scope.template = "/static/eventsTrackList.html";
}

function SetlistCtrl($scope, $http, $resource) {
    /* Protection against cross site scripting attacks. */
    $http.defaults.headers.post['X-CSRFToken'] = csrftoken;

    var Track = $resource("/api/:event/:action/:track/",
        {action: "get-track-list", event: ps.event},
        {vote: {
            method: 'POST',
            params: { action: "vote", track: '@pk'}
               }
        }
    );

    var lastfmTrack = $resource("http://ws.audioscrobbler.com/2.0/?method=track.:action&api_key="+ps.LAST_FM_API_KEY+"&format=json",
      {action: "getInfo", track: "", artist: ""}
    );

    // GET: /api/123/get-track-list
    $scope.setlist = Track.query({}, function(data){
        console.log("Received setlist, asking last.fm for covers...");
        for(i=0; i<data.length; i++){
            findCover(data[i]);
        }
    });

    $scope.vote = function(track, isUpVote) {
        console.log("Got a vote!");
        track.$vote({vote: isUpVote});
    }

    function findCover(track){
        lastfmTrack.get(
            {track: track.name, artist: track.artist},
            function(data){
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
                if(data.hasOwnProperty("track")){
                    var albumImages = data.track.album.image;
                    // Select the largest one...
                    track.coverURL = albumImages[albumImages.length - 1]['#text'];
                }
            }
        );
    }

}
