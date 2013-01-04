package party.sense.app;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

public class SplashActivity extends Activity {

	private static final String TAG = "com.partysense.app.SplashActivity";
	
	/** Called when the activity is first created. */
	@Override

	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.splash);
		ArrayList<Club> clubs = new ArrayList<Club>();
		
		/*Thread splashTimerThread = new Thread(){
			public void run(){
				try{
					clubs = this.updateClubs();
					int counter = 0;
					while()
					{
						Thread.currentThread().sleep(1000);
						sleep(100);
						counter += 100;
					}
					startActivity(new Intent("android.intent.action.PartySenseMainActivity"));
					
				} catch(IOException exception){
					Log.e(TAG, exception.getMessage());
				} catch (InterruptedException e) {
					e.printStackTrace();
				} catch (ExecutionException e) {
					e.printStackTrace();
				}
				finally{
					finish();
				}
			}
		};
		splashTimerThread.start();
		*/
		
		try {
			clubs = this.updateClubs();
			while( clubs == null){
				Thread.currentThread().sleep(100);
				Log.e("Splash Activity","Waiting for Clubs List from Task");
			}
			Bundle b = new Bundle();
			b.putParcelableArrayList("party.sense.app.clubsList", clubs);
			Intent i = new Intent(this, PartySenseMainActivity.class);
			i.putExtras(b);
			startActivity(i);

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


