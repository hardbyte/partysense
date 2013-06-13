'use strict';

/* Filters */

angular.module('ps.filters', [])
  .filter('removeAddedTracks', function() {
  return function(allTracks) {
      if(allTracks) {
          // TODO this is quite expensive!
          // If the track has the same artist, the name can't be too similar?
          // Artists like Mumford & Sons release "Little Lion Man" on multiple
          // albums and Spotify has seperate instances of those tracks.
          // The external ids and the names match though.
          // Also want to ensure we keep one of them!
          console.log("Removing duplicates. Original length = " + allTracks.length);
          allTracks = allTracks.filter(function(track, i, array){
              return !array.some(function(innerTrack, j){
                  return i > j && i !== j && track.name === innerTrack.name;
              });
          });
          console.log("After removing duplicates length = " +allTracks.length );
      }
      // each
      return allTracks;
  };
});