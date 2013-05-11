angular.module('Partysense', ['ngResource']);


function SpotifyTemplateCtrl($scope) {
    $scope.template = "/static/spotifyResultList.html";
}
function PreviewTemplateCtrl($scope) {
    $scope.template = "/static/spotifyPreview.html";
}

function SetlistTemplateCtrl($scope) {
    $scope.template = "/static/eventsTrackList.html";
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

    $scope.clear = function() {
        $scope.spotifyResult = "";
        $scope.searchTerm = "";
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


function SetlistCtrl($scope, $http, $resource) {
    /* Protection against cross site scripting attacks. */
    $http.defaults.headers.post['X-CSRFToken'] = csrftoken;

    var Track = $resource("/api/:event/:action/:track/",
        {action: "get-track-list", event: ps.event},
        { }
    );

    var lastfmTrack = $resource("http://ws.audioscrobbler.com/2.0/?method=track.:action&api_key="+ps.LAST_FM_API_KEY+"&format=json",
      {action: "getInfo", track: "", artist: ""}
    );

    // GET: /api/123/get-track-list
    $scope.setlist = Track.query({}, function(data){
        console.log("Received setlist, asking last.fm for covers...");
        var songs = "";
        for(i=0; i<data.length; i++){
            findCover(data[i]);
            songs += data[i].spotifyTrackID.slice(14) + ',';
        }
        $scope.playlistSongs = songs;
    });


    for(i=0; i < $scope.setlist.length; i++){

    }
    // encode the events name in the spotify playlist
    $scope.playlistName = encodeURIComponent("Partysense - " + ps.eventTitle);

    $scope.vote = function (track, isUpVote) {
        console.log("Got a vote!");
        console.log(track);
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
                if(data.hasOwnProperty("track") && data.track.hasOwnProperty("album")){
                    var albumImages = data.track.album.image;
                    // Select the largest one...
                    track.coverURL = albumImages[albumImages.length - 1]['#text'];
                }
            }
        );
    }

}
