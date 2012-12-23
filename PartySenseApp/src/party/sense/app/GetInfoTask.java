package party.sense.app;

import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

import android.os.AsyncTask;
import android.util.Log;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.google.gson.stream.JsonReader;

class GetInfoTask extends AsyncTask<String, Void, List<Club>> {

    private Exception exception;

    protected List<Club> doInBackground(String... urls) {
    	Log.i("GetInfoTask", "Starting");
        try {
        	Gson gson = new Gson();
        	String fetchUrl = (String)urls[0];
            URLConnection urlConnection =  new URL(fetchUrl).openConnection();
            urlConnection.connect();
            JsonReader reader = new JsonReader(
                 new InputStreamReader(urlConnection.getInputStream()));
            JsonParser parser = new JsonParser();
            JsonArray infoArray = parser.parse(reader).getAsJsonArray();
            List<Club> clubs = new ArrayList<Club>();
            String clubnames = "";
            for (JsonElement element: infoArray){
            	Club club = gson.fromJson(element, Club.class);
            	clubs.add(club);
            }
            return clubs;
            
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