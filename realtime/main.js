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
                console.log("Client closed connection");
            });
        });
  });


});

