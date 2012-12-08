package party.sense.app;

import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

import android.os.AsyncTask;
import android.util.Log;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.google.gson.stream.JsonReader;

class GetInfoTask extends AsyncTask<String, Void, String> {

    private Exception exception;

    protected String doInBackground(String... urls) {
        try {
        	Gson gson = new Gson();
        	String fetchUrl = (String)urls[0];
            URLConnection urlConnection =  new URL(fetchUrl).openConnection();
            urlConnection.connect();
            JsonReader reader = new JsonReader(
                 new InputStreamReader(urlConnection.getInputStream()));
            JsonParser parser = new JsonParser();
            JsonElement greeting = parser.parse(reader);
            HelloWorld myHelloWorld = gson.fromJson(greeting, HelloWorld.class);
            String message = myHelloWorld.getMessage();
            Log.e("GetInfoTask", message);
            return message;
            
        } catch (Exception exception) {
            this.exception = exception;
            return null;
        }
    }

    protected void onPostExecute(String greeting) {
        // TODO: check this.exception 
        // TODO: do something with the info
    }

 }