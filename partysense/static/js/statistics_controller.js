

angular.module('Partysense')
  .controller('EventStatsCtrl', ['$scope', '$log',
        "Track", "SpotifyPlayer", "updateService", "Amazon", "websocket",
  function($scope, $log, Track, SpotifyPlayer, updateService, Amazon, websocket) {
    "use strict";
    $scope.setlist = ps.setlist;

    $scope.updates = [
        // example object for testing:
        //{"eid":1,"event":"B-rave","track":"Blue Ocean Floor","artist":"Justin Timberlake","tid":1,"up":true}
        ];

    websocket({'event': "ALL"}, $scope.updates);


    $scope.refreshTracks = function(){
        // GET: /api/123/get-track-list
        //$scope.setlist = Track.query({action: "get-track-list"}, function(data){

        var data = ps.setlist;
        $scope.selectedTracks = [];
        $scope.selectAll = false;
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

        $scope.toggleAll = function(){
            $scope.popularTracks.forEach(function(track){
                track.selected = $scope.selectAll;
            });
        };

        function getSelectedTracks(){
            return $scope.popularTracks.filter(function(t){return t.selected;});
        }

        $scope.tracksSelected = function(){
            return getSelectedTracks().length > 0;
        };

        $scope.playInSpotify = function(){
            // Get the selected tracks
            $log.info("Opening in Spotify");
            var tracks = getSelectedTracks();

            // Choice here to provide a URL or URI
            // URL goes to open.spotify.com, URI directly launches app
            //return SpotifyPlayer.getPlaylistURI(tracks, "Popular Tracks");
            return SpotifyPlayer.getPlaylistURL(tracks, "Popular Tracks");

//            var link = document.createElement("a");
//            link.setAttribute("href", SpotifyPlayer.getPlaylistURL(tracks, "Partysense"));
//            //link.setAttribute("target", "_blank");
//            link.click();
        };

        $scope.buyOnAmazon = function(){
            // Currently this just adds the "offer" to the Track object
            // TODO: Needs backend change to support shopping cart
            $log.info("Filtering tracks to purchase");
            Amazon.showTrackOffers(getSelectedTracks());
        };

        $scope.download = function(){
            // Create a csv file and "download" it
            var tracks = getSelectedTracks();
            var csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "Title,Artist,Votes\n";
            tracks.forEach(function(track, index){
                var dataString = track.name + "," + track.artist +
                                 ',' + (track.upVotes - track.downVotes);
                csvContent += index < tracks.length ? dataString + "\n" : dataString;
            });

            var encodedUri = encodeURI(csvContent);

            var link = document.createElement("a");
            var filename = "partysense_tracks.csv";
            if('download' in link){
                // We are probably in Chrome
                link.setAttribute("href", encodedUri);
                link.setAttribute("download", filename);
                document.body.appendChild(link);
                link.click(); // This will download the data file named "my_data.csv".
            } else {

                var blob = new Blob([csvContent],{
                    type: "text/csv;charset=utf-8;"
                });

                if('msSaveBlob' in navigator){
                    navigator.msSaveBlob(blob, filename);
                } else {
                    window.open(encodedUri, '_blank', '');
                }



            }
        };
    };

    $scope.refreshTracks();
}]);