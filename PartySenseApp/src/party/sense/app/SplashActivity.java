package party.sense.app;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.opengl.Visibility;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class SplashActivity extends Activity {
	SharedPreferences settings;
	private static final String TAG = "com.partysense.app.SplashActivity";
	public static final String BUNDLE_ID_CLUBS_LIST = "party.sense.app.clubsList";
	Intent i;
	Button btnLogin;
	TextView txtLogin;
	/** Called when the activity is first created. */
	@Override

	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.splash);
		ArrayList<Club> clubs = new ArrayList<Club>();
		settings = getSharedPreferences(FragmentMenuScreen.PREFS_NAME, 0);
		
		btnLogin = (Button) findViewById(R.id.btnLogin);
		String loginName = settings.getString(getResources().getString(R.string.pref_name_on_facebook),null);
		Thread splashTimerThread = new Thread(){
			public void run(){
				try{
					int counter = 0;
					while(counter<5)
					{
						Thread.sleep(1000);
						counter += 1;
					}
				}
				catch(Exception e){
				}
				finally{
					startActivity(i);
					finish();
				}
			}
		};
		
		try {
			clubs = this.updateClubs();
			while( clubs == null){
				Log.e("Splash Activity","Waiting for Clubs List from Task");
			}
			Bundle b = new Bundle();
			b.putParcelableArrayList("party.sense.app.clubsList", clubs);
			i = new Intent(this, PartySenseMainActivity.class);
			i.putExtras(b);
			
			//Logic to set login
			if (loginName != null){
				txtLogin.setVisibility(View.INVISIBLE);
				btnLogin.setVisibility(View.VISIBLE);
			}
			else{
				txtLogin.setText("You are logged in as:" + loginName);
				txtLogin.setVisibility(View.VISIBLE);
				btnLogin.setVisibility(View.INVISIBLE);
				splashTimerThread.start();
			}
			
			

		} catch(IOException exception){
			Log.e(TAG, exception.getMessage());
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		}

	}

	/**
	 * Temporary method to Test Android JSON capability
	 * @throws IOException 
	 * @throws ExecutionException 
	 * @throws InterruptedException
	 * @return List of Clubs  
	 */
	public ArrayList<Club> updateClubs() throws IOException, InterruptedException, ExecutionException {
		String fetchUrl = "http://partysenseapp.appspot.com/api/clubs-dump";
		Log.e(TAG, "Going to Execute task");
		ArrayList<Club> clubs = new GetClubsListTask(this.getApplicationContext(), "").execute(fetchUrl).get();
		String clubInfo = ""; 
		for (Club club : clubs) {
			clubInfo += club.getName() + " ";
			List<String> tagList = club.getTags();
			clubInfo += "{";
			for (String tag : tagList){
				clubInfo += (tag + " ");
			}
			clubInfo += "}";
		}
		//Log.e(TAG, "Got Clubs List : " + clubInfo);
		return clubs;
	}
}


	/*
	// Adding functionality to Read/ Write to internal storage
	String myString = "Testing writing to Club DB";

	//File filesDirectory = this.getDir("files", Context.MODE_PRIVATE); //Creating an internal dir;
	try {
		FileOutputStream out = openFileOutput("clubDbTest.json", Context.MODE_PRIVATE);
		out.write(myString.getBytes());
		out.close();
	} catch (FileNotFoundException fnfe) {
		fnfe.printStackTrace();
	} catch (IOException ioe) {
		ioe.printStackTrace();
	}

	FileInputStream in = null;
	try {
		in = openFileInput("clubDbTest.json");
	} catch (FileNotFoundException e) {
		e.printStackTrace();
	}
	InputStreamReader inputStreamReader = new InputStreamReader(in);
	BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
	String line = null;
	try {
		line = bufferedReader.readLine();
	} catch (IOException ioe) {
		ioe.printStackTrace();
	}
	Log.e( TAG, "Read : " + line);

	/*StringBuilder sb = new StringBuilder();
    try {
		while ((line = bufferedReader.readLine()) != null) {
		    sb.append(line);
		}
		Log.e("SplashActivity", "Read : " + line);
		bufferedReader.close();
	} catch (IOException e) {
		e.printStackTrace();
	}*/


