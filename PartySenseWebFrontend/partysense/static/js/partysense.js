var App = angular.module('Partysense',
  ['ngResource', 'ps.filters', 'ps.services', 'ps.directives']);

/* Template Controller will pull in all the other HTML fragments
 * and the other Angular Controllers. I haven't used routes. */
App.
  controller('TemplateCtrl', ['$scope', function($scope) {
        "use strict";
        $scope.oneAtATime = true;
        $scope.loggedIn = ps.loggedIn;
        $scope.resultListTemplate = "/static/partials/searchResults.html";
        $scope.previewTemplate = "/static/partials/spotifyPreview.html";
        $scope.setlistTemplate = "/static/partials/eventsTrackList.html";
        $scope.recentTracksTemplate = "/static/partials/recentTrackList.html";
        $scope.eventStatisticsTemplate = "/static/partials/eventStatistics.html";
  }]);


App.controller('RecentTrackCtrl', ['$scope', 'Track', 'updateService', function($scope, Track, updateService) {
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
}]);
