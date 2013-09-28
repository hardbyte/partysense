

angular.module('Partysense')
  .controller('EventStatsCtrl', ['$scope', "Track", "updateService",
  function($scope, Track, updateService) {
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
}]);