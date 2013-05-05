package party.sense.app;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.concurrent.ExecutionException;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
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
		txtLogin = (TextView) findViewById(R.id.txtLogin);
		btnLogin = (Button) findViewById(R.id.btnLogin);
		
		String loginName = settings.getString(getResources().getString(R.string.pref_name_on_facebook),null);
		final Thread splashTimerThread = new Thread(){
			public void run(){
				try{
					int counter = 0;
					while(counter<1)
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
		
		
		btnLogin.setOnClickListener(new OnClickListener() {
					
					public void onClick(View v) {
						splashTimerThread.start();
						
					}
		});
		
		try {
			

			clubs = this.updateClubs();
			while( clubs == null){
				Log.e("Splash Activity","Waiting for Clubs List from Task");
			}
			
			Log.e("Splash Activity",Integer.toString(clubs.size()));
			
			Bundle b = new Bundle();
			b.putParcelableArrayList("party.sense.app.clubsList", clubs);
			i = new Intent(this, SetupActivity.class);
			i.putExtras(b);
			
			//Logic to set login
			if (loginName != "null"){
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
		Calendar calendar = Calendar.getInstance();
		String apiRequestBaseUrl = "http://partysenseapp.appspot.com/api/clubs-delta";
		//String apiRequestParams = "/year/" + calendar.get(Calendar.YEAR) + "/month/" + calendar.get(Calendar.MONTH) + "/day/"+ calendar.get(Calendar.DAY_OF_MONTH);
		String apiRequestParams = "/year/2012/month/04/day/01";
		String fetchUrl = apiRequestBaseUrl + apiRequestParams;
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
		Log.e(TAG, "Got Clubs List : " + clubInfo);
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


