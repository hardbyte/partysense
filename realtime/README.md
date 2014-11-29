
The realtime API heavily leverages our postgres database. It won't work on a local install with sqlite3.





# Database modifications

The database needs two modifications to setup notifications. The channels are:
- `event-<ID>`
- `firehose`

Note channel `firehose` is more of a gentle trickle.


## Notification Functions

This psql function will "NOTIFY" any listening clients on a given channel (`firehose`). The client in this case will be the lightweight nodejs app.
    
    CREATE FUNCTION notify_firehose() RETURNS trigger AS $$
    DECLARE
      eid integer := 0;
      track music_view%ROWTYPE;
      event event_event%ROWTYPE;
    BEGIN
      eid := NEW.event_id;
      SELECT * INTO track FROM music_view WHERE id=NEW.track_id;
      SELECT * INTO event FROM event_event WHERE id=eid;
      PERFORM pg_notify('firehose', '{"eid": '|| eid || ', "event": "' || event.title || '", "track": "' || track.name || '", "artist": "' || track.artist || '", "tid": ' || NEW.track_id || ', "up":' || NEW.is_positive || '}' );
      RETURN new;
    END;
    $$ LANGUAGE plpgsql;

It has some rather brittle json formating code, in newer versions of postgresql there is a `row_to_json` function which
would be a better idea than string formatting.

And similar for the event specific watchers:

    CREATE FUNCTION notify_trigger() RETURNS trigger AS $$
    DECLARE
      eid integer := 0;
      track music_view%ROWTYPE;
    BEGIN
      eid := NEW.event_id;
      SELECT * INTO track FROM music_view WHERE id=NEW.track_id;
      PERFORM pg_notify('event_' || eid, '{"track": "' || track.name || '", "artist": "' || track.artist || '", "tid": ' || NEW.track_id || ', "up":' || NEW.is_positive || '}' );
      RETURN new;
    END;
    $$ LANGUAGE plpgsql;


## Trigger

Lastly a trigger must be set up on each table to call the notification function.

    CREATE TRIGGER my_trigger AFTER INSERT ON event_vote FOR EACH ROW EXECUTE PROCEDURE notify_trigger()
    
    CREATE TRIGGER firehose_trigger AFTER INSERT ON event_vote FOR EACH ROW EXECUTE PROCEDURE notify_firehose()

# Nodejs App

This needs an open port on the server, and a static IP address so we can connect websockets to it.


    var pg = require('pg');
    var WebSocketServer = require('ws').Server;
    
    var databaseConfig = {
          user: 'partysense',
          password: 'fV#BXd!aKPNAL0h',
          database: 'pstest',
          host: 'localhost',
          port: 5432
        };
    
    
    var wss = new WebSocketServer({port: 18854});
    
    wss.on('connection', function(ws) {
        console.log("New websocket connected");
        console.log("Waiting for stream configuration message");
    
        ws.on('message', function(e){
            var channel;
            console.log(e);
            console.log("Received the config:");
            var m = JSON.parse(e);
            console.log(m);
            var event_id = m.event;
            if(event_id === "ALL"){
                channel = "firehose";
            } else {
                channel = "event_" + event_id;
            }
    
            console.log("Channel: " + channel);
    
            // Now we connect to the database
            var client = new pg.Client(databaseConfig);
            client.connect(function(err) {
                if(err) {
                    console.log("Couldn't connect to the database :-/");
                    console.log(err);
                }
                console.log("Registering for the 'event_" + event_id + "' channel");
                client.on('notification', function(msg) {
                    console.log("Message received!");
                    console.log(msg.payload);
                    ws.send(msg.payload, function(e){
                        // if error is null, the send has been completed,
                        // otherwise the error object will indicate what failed.
                        if(e) {
                            console.log(e);
                        }
                    });
    
                });
    
                client.query("LISTEN " + channel);
                console.log("Waiting for notifications on channel: " + channel);
    
                ws.on("close", function(){
                    // Probably not required but could help avoid memory leak
                    client.query("UNLISTEN " + channel);
                    client.end();
                });
            });
      });
    
    });
    
# WWW client

An example client that simply connects to the firehose websocket:
    
    <!DOCTYPE html>
    <html>
    <head lang="en">
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
    <h1>Live stream for event 1:</h1>
    <ol id="data">
    
    </ol>
    <script>
        var el = document.getElementById("data");
        var s = new WebSocket("ws://108.168.154.105" + ":18854");
    
        s.onopen = function (e) {
            console.log("connected new socket for event stream");
            s.send(JSON.stringify({
                //'event': 1
                'event': "ALL"
            }));
        };
    
        s.onmessage = function(e){
            var m = JSON.parse(e.data);
            console.log("Received:");
            console.log(m);
    
            var li = document.createElement("li");
            li.innerText = m.track + " by " + m.artist + " was voted " + (m.up ? "up" : "down");
            el.appendChild(li);
        };
    </script>
    </body>
    </html>