/* Services */

angular.module('ps.services', ['ngResource'])
  .factory("Amazon", ["$http", "$log", function ($http, $log) {
      "use strict";
      return {
          showTrackOffers: function (tracks) {
              /* Query multiple tracks prices at once.
              * Modifies the track objects to contain an *offer* object
              * which has an url and price.
              * */

              var trackIds = tracks.map(function(track){return track.pk;});

              $http.get("/amazon/multiple/?pks=" + JSON.stringify(trackIds))
                .success(function (response) {
                    if (response.error) {
                        $log.warn("An error occurred while retrieving prices from amazon");
                    } else {
                        //$log.info("Received multiple amazon prices");
                        for (var i = 0; i < tracks.length; i++) {
                            var track = tracks[i];
                            track.offer = {
                                url:   response[track.pk].URL,
                                price: response[track.pk].price
                            };
                        }
                    }
                })
                .error(function (response) {
                    $log.error("Awkward error...");
                });

          },
          showTrackOffer:  function (track) {
              /* This is used to query amazon for the price of a single track */
              track.offer = {};

              $http.get("/amazon/single/?artist=" + track.artist + "&track=" + track.name + "&pk=" + track.pk)
                .success(function (response) {
                    if (response.error) {
                        track.offer = {
                            "error": response.error
                        };
                    } else {
                        track.offer = {
                            url:   response.URL,
                            price: response.price
                        };
                    }
                })
                .error(function (response) {
                    $log.error("Got an error...");
                    track.offer = {
                        "error": "Sorry, an error occurred"
                    };
                });

          }

      };
  }])
  .factory("SpotifyPlayer", ['$sce', function ($sce) {
      "use strict";
      /* The SpotifyPlayer service exposes several functions
      for linking to spotify playlists, embedding iframe players.

      The functions all assume that tracks have a *spotifyTrackID*
      attribute in the form: "spotify:track:5YNFRKdTj5JG18ZWNDPDnD"

      */

      function getSpotifyIDs(tracks) {
          var ids = [];
          for (var i = 0; i < Math.min(80, tracks.length); i++) {
              ids.push(tracks[i].spotifyTrackID.slice(14));
          }
          return ids;
      }

      function getSpotifyURI(tracks, title){
          /* Returns a uri to be used as part of a href */

          var spotifyTracks = getSpotifyIDs(tracks).join(",");
          var playlistName = encodeURIComponent(title);
          return "spotify:trackset:" + playlistName + ":" + spotifyTracks;
      }

      return {
          getPlaylistURI: getSpotifyURI,
          getPlaylistURL: function(tracks, title){
              return "http://open.spotify.com/trackset/" +
                encodeURIComponent(title) + "/" +
                getSpotifyIDs(tracks).join(",");
          },
          getIFramePlayer: function (tracks, eventTitle) {
              /* Return safe html for a Spotify iframe player
               * Only uses first 80 tracks due to Spotify limitation.
               * */

              var uri = getSpotifyURI(tracks, "Partysense Playlist - " + eventTitle);

              var spotifyPlaylistURL = "https://embed.spotify.com/?uri=" +
                                       uri + "&view=list";
              return $sce.trustAsHtml(
                '<iframe src="' + spotifyPlaylistURL +
                '" frameborder="0" allowtransparency="true" width="100%" height="380"></iframe>');
          }
      };
  }])
  .factory('SpotifySearch', function ($http, $resource) {
      /* Protection against cross site scripting attacks. */
      $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
      return $resource("http://ws.spotify.com/search/1/:action",
        {action: 'track.json', q: 'artist:Gaga'}
      );
  })
  .factory('SpotifyLookup', function ($http) {
      /* When we know exactly what we're after from Spotify. */
      // http://stackoverflow.com/questions/11850025/recommended-way-of-getting-data-from-the-server
      var SpotifyLookup = function (data) {
          angular.extend(this, data);
      };

      // static method to retrieve spotify stuff by URI
      SpotifyLookup.get = function (uri) {
          return $http.get("http://ws.spotify.com/lookup/1/.json?uri=" + uri)
            .then(function (response) {
                return new SpotifyLookup(response.data);
            });
      };

      return SpotifyLookup;
  })
  .factory('Track',function ($http, $resource) {
      /* This is the partysen.se api */
      /* Protection against cross site scripting attacks. */
      $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
      return $resource("/api/:event/:action/:track",
        {action: "modify", event: ps.event}
      );
  }).factory('LastfmTrack', function ($http, $resource) {
      return $resource("http://ws.audioscrobbler.com/2.0/?method=track.:action&api_key=" + ps.LAST_FM_API_KEY + "&format=json",
        {action: "getInfo", track: "", artist: ""}
      );
  })
  .factory('updateService', function ($rootScope) {
      return {
          update: function (event, args) {
              console.log("Passing on event: " + event);
              console.log(args);
              $rootScope.$broadcast(event, args);
          }
      };
  });