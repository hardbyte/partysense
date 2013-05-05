package party.sense.app;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.nio.channels.FileChannel;
import java.util.ArrayList;

import android.content.Context;
import android.os.AsyncTask;
import android.os.Environment;
import android.util.Log;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.google.gson.stream.JsonReader;

/**
 * Async Task to fetch a list of clubs from the database (web or local)
 * @author Tanmay Bhola [tanmay9@gmail.com]
 *
 */
class GetClubsListTask extends AsyncTask<String, Void, ArrayList<Club>> {
	
	private static final String TAG = "com.party.sense.app.GetInfoTask";
    private Exception exception;
    private Context context;
    private String regionKey; // TODO: is this required ? 
    
    /**
     * Constructor for GetClubsListTask
     * @param context The application context
     * @param regionKey The key for the city/ region the person is using the app from
     */
    public GetClubsListTask(Context context, String regionKey){
    	this.context = context;
    	this.regionKey= regionKey;
    }
    
    /*
     * Method to do the background task of fetching information from the backend or local database 
     * (non-Javadoc)
     * @see android.os.AsyncTask#doInBackground(Params[])
     */
    protected ArrayList<Club> doInBackground(String... urls) {
    	Log.e("GetInfoTask", "Starting");
    	ArrayList<Club> clubs = new ArrayList<Club>();
    	try {
    		Gson gson = new Gson();
    		String fetchUrl = (String)urls[0];
            URLConnection urlConnection =  new URL(fetchUrl).openConnection();
            urlConnection.connect();
            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            String inputLine;
            FileOutputStream out = null;

            out = this.context.openFileOutput("clubDbTest.json", Context.MODE_PRIVATE);
            while((inputLine = in.readLine()) != null){
            	out.write(inputLine.getBytes());
            }
            out.close();
            Log.e(TAG , "Finished Writing to json File");
    		
    		
    		// Create a Connection to the local storage
    		URLConnection localConnection = new URL("file:///data/data/party.sense.app/files/clubDbTest.json").openConnection();
    		localConnection.connect();
    		JsonReader reader = new JsonReader(
    				new InputStreamReader(localConnection.getInputStream()));
    		JsonParser parser = new JsonParser();
    		JsonArray infoArray = parser.parse(reader).getAsJsonArray();
    		String clubnames = "";
    		for (JsonElement element: infoArray){
    			Club club = gson.fromJson(element, Club.class);
    			clubs.add(club);
    		}
    		reader.close();

    	} catch(MalformedURLException mue){
    		Log.e(TAG, "MalformedUrlException in trying to open the URL : " + mue.getMessage());
    	}  catch (FileNotFoundException fnfe) {
			fnfe.printStackTrace();
		} catch (IOException ioe) {
			ioe.printStackTrace();
		} 

    	return clubs;
    }

    protected void onPostExecute(String greeting) {
        // TODO: check this.exception 
        // TODO: do something with the info
    	Log.i("GetClubInfoTask", "Completed");
    }

 }