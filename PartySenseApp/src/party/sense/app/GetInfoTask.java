package party.sense.app;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.google.gson.stream.JsonReader;

/**
 * Class to 
 * @author tanmaybhola
 *
 */
class GetInfoTask extends AsyncTask<String, Void, List<Club>> {
	
	private static final String TAG = "com.party.sense.app.GetInfoTask";
    private Exception exception;
    private Context context;
    private String regionKey; // TODO: is this required ? 
    
    /**
     * Constructor for GetInfoTask
     * @param context The application context
     */
    public GetInfoTask(Context context, String regionKey){
    	this.context = context;
    	this.regionKey= regionKey;
    }
    
    protected List<Club> doInBackground(String... urls) {
    	Log.i("GetInfoTask", "Starting");
        try {
        	Gson gson = new Gson();
        	String fetchUrl = (String)urls[0];
            URLConnection urlConnection =  new URL(fetchUrl).openConnection();
            urlConnection.connect();
            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            String inputLine;
            FileOutputStream out = null;
            try {
    			out = this.context.openFileOutput("clubDbTest.json", Context.MODE_PRIVATE);
    			while((inputLine = in.readLine()) != null){
    				out.write(inputLine.getBytes());
    			}
    			out.close();
    			Log.e(TAG , "Finished Writing to json File");
    		} catch (FileNotFoundException fnfe) {
    			fnfe.printStackTrace();
    		} catch (IOException ioe) {
    			ioe.printStackTrace();
    		}
    		//UrlConnection localConnection = new URL()
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
            in.close();
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