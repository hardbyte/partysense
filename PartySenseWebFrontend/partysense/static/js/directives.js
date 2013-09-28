/* Angular Directives */

/* Allow a background image */
angular.module('ps.directives', [])
  .directive('backImg', function(){
    return function(scope, element, attrs){
        attrs.$observe('backImg', function(value) {
            element.css({
                'background-image': 'url(' + value +')',
                //'background-size' : 'cover',
                'background-position' : 'right',
                'background-repeat' : 'no-repeat'
            });
        });
    };
  })

  .directive('droppable', function($compile, $rootScope, updateService) {
    "use strict";
    /* This allows importing from spotify via drag and drop. */
    return {
        restrict: "A",
        //The link function is responsible for registering DOM listeners as well as updating the DOM.
        link: function(scope, element, attrs){

            element.context.ondragover = function(event) {
                // TODO maybe we can work out if this is from spotify here?
                if(true){
                    // Do something to show we can deal with items dropped on this
                    element.addClass("indicate-drop");
                    return false;
                } else {
                    console.log("I don't know how to deal with that... should I?");
                    console.log(event);
                }
            };

            element.context.ondragleave = function(event){
                attrs.$set('class', '');
            };

            element.context.ondrop = function (event) {
                // work out if this is something we can deal with...
                // get an open url:
                //http://open.spotify.com/user/1242959390/playlist/4rN0f6C22Mz9dUX5lcbG5F
                var open_url = event.dataTransfer.getData("text/plain");
                console.log("open url: " + open_url);
                if(/.*spotify.*/.test(open_url)){

                    var uri = event.dataTransfer.getData("text/uri-list");
                    console.log("uri: " + uri);
                    // sometimes like this:
                    //spotify:user:1242959390:playlist:4rN0f6C22Mz9dUX5lcbG5F

                    //console.log(event.dataTransfer.getData("text/html"));
                    // <a href="http://open.spotify.com/user/1242959390/playlist/4rN0f6C22Mz9dUX5lcbG5F">Trial</a>

                    var el = document.createElement( 'div' );
                    el.innerHTML = event.dataTransfer.getData("text/html");
                    var name = el.innerText;
                    console.log("Name: " + name);

                    var type = "unknown";

                    if(/.*playlist.*/g.test(uri)){
                        console.log("Looks like " + uri + " is a playlist");
                        type = "playlist - I can't import that from spotify sorry";
                    }
                    if(/.*album.*/g.test(uri)) {
                        type = "album";
                        $rootScope.$apply(function(){
                            updateService.update("importAlbumBySpotifyURI", uri);
                        });
                    }
                    if(/.*artist.*/.test(uri)) {
                        //console.log("Looks like " + uri + " is an artist");
                        type = "artist";
                        /* The html already has the artist name, so lets just use that... (is that a hack?)*/

                        var artist = {name: name, href: uri};
                        // IMPORTANT to call $apply to force AngularJS to notice that we change stuff!
                        $rootScope.$apply(function(){
                            updateService.update("searchByArtist", artist);
                        });

                    }
                    if(/.*track.*/.test(uri)) {
                        console.log("Looks like " + uri + " is a track");
                        type = "track";
                        $rootScope.$apply(function(){
                            console.log("Sending broadcast...");
                            updateService.update("addTrackBySpotifyURI", uri);
                        });
                    }

                    // Send a message letting the user know what we are doing
                    $rootScope.$apply(function(){
                        updateService.update("showMsg",
                            "Importing Spotify " + type + " - " + name + ".");
                    });

                    // Seems if I don't preventDefault then spotify will start playing...
                    event.preventDefault();

                    // Remove the extra class we added to show this accepts dropping stuff
                    attrs.$set('class', '');
                    //return false;
                }
            };
        }
    };
});
