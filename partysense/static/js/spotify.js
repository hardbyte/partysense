angular.module('Spotify', ['ngResource']);



function Ctrl($scope) {
    $scope.template = "/static/spotifyResultList.html";
}

function SpotifyCtrl($scope, $http, $resource) {
    /* Protection against cross site scripting attacks. */
    $http.defaults.headers.post['X-CSRFToken'] = csrftoken;

    /* Resources */ $scope.spotify = $resource("http://ws.spotify.com/search/1/:action",
      {action: 'track.json', q:'Gaga'}
    );



    var Track = $scope.api = $resource("/api/:event/modify",
      {event: ps.event}
    );

    $scope.doSearch = function() {
        console.log("Searching spotify for: " + $scope.searchTerm);
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
        console.log(newTrack);
        newTrack.$save(function(track, putResponseHeaders){
            console.log("Saved a new track...");
            updateTrackView();
        });

        // todo add class "icon-white" to that element's icon

    };
}

