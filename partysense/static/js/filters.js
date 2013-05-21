'use strict';

/* Filters */

angular.module('ps.filters', [])
  .filter('removeAddedTracks', function() {
  return function(allTracks) {
      //console.log("In filter.");
      //console.log(allTracks);
      // each
      return allTracks;
  };
});