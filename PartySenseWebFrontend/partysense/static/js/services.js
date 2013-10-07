/* Services */

angular.module('ps.services', ['ngResource'])
   .factory('SpotifySearch', function($http, $resource){
        /* Protection against cross site scripting attacks. */
        $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
        return $resource("http://ws.spotify.com/search/1/:action",
            {action: 'track.json', q:'artist:Gaga'}
        );
    })
   .factory('SpotifyLookup', function($http){
      /* When we know exactly what we're after from spotify. */
      // http://stackoverflow.com/questions/11850025/recommended-way-of-getting-data-from-the-server
      var SpotifyLookup = function(data){
          angular.extend(this, data);
      };

      // static method to retrieve spotify stuff by URI
      SpotifyLookup.get = function(uri){
          return $http.get("http://ws.spotify.com/lookup/1/.json?uri=" + uri)
            .then(function(response){
                return new SpotifyLookup(response.data);
            });
      };

      return SpotifyLookup;
    })
  .factory('Track', function($http, $resource){
      /* This is the partysen.se api */
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