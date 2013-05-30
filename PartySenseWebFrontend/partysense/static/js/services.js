/* Services */

angular.module('ps.services', ['ngResource'])
   .factory('SpotifySearch', function($http, $resource){
        /* Protection against cross site scripting attacks. */
        $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
        return $resource("http://ws.spotify.com/search/1/:action",
            {action: 'track.json', q:'artist:Gaga'}
        );
    })
  .factory('Track', function($http, $resource){
      /* Protection against cross site scripting attacks. */
      $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
      return $resource("/api/:event/:action/:track",
        {action: "modify", event: ps.event}
    );
  }).factory('LastfmTrack', function($http, $resource){
      return $resource("http://ws.audioscrobbler.com/2.0/?method=track.:action&api_key="+ps.LAST_FM_API_KEY+"&format=json",
      {action: "getInfo", track: "", artist: ""}
    );
  })
  .factory('updateService', function($rootScope) {
      return {
          update: function(event, args){
              console.log("Passing on event: " + event);
              console.log(args);
              $rootScope.$broadcast(event, args);
          }
      };
  });