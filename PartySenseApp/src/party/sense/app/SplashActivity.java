package party.sense.app;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.concurrent.ExecutionException;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.facebook.Session;
import com.facebook.SessionState;
import com.facebook.UiLifecycleHelper;

public class SplashActivity extends FragmentActivity {
	
	private static final String TAG = "SplashActivity";
	public static final String PREFS_NAME = "PartySenseSharedPreferences";
	public static final String BUNDLE_ID_CLUBS_LIST = "party.sense.app.clubsList";
	private SharedPreferences settings;
	private SharedPreferences.Editor edit;
	
	private static final int LOGIN = 0;
	private static final int WELCOME = 1;
	private static final int FRAGMENT_COUNT = WELCOME + 1;
	private Fragment[] fragments = new Fragment[FRAGMENT_COUNT];
	private FragmentManager fm;
	
	private Intent i;
	
	private boolean isResumed = false;
	
	private UiLifecycleHelper uiHelper;
	private Session.StatusCallback callback = new Session.StatusCallback() {

		public void call(Session session, SessionState state, Exception exception) {
			onSessionStateChange(session, state, exception);
		}
	};
	
	
	private final Thread splashTimerThread = new Thread(){
		public void run(){
			try{
				int counter = 0;
				// Keep looping until timer expires and next activity intent is set
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
	
	/** Called when the activity is first created. */
	@Override

	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.layout_splash_activity);
		ArrayList<Club> clubs = new ArrayList<Club>();
		//btnLogin = (Button) findViewById(R.id.btnLogin);
		DBactions db = new DBactions(getApplicationContext());
		
		settings = getSharedPreferences(this.PREFS_NAME, 0);
		
		// This creates a Facebook session and opens is automatically if a 
		// cached token is available
		uiHelper = new UiLifecycleHelper(this, callback);
		uiHelper.onCreate(savedInstanceState);
		
		FragmentManager fm = getSupportFragmentManager();
		fragments[LOGIN] = fm.findFragmentById(R.id.facebookLoginFragment);
		fragments[WELCOME] = fm.findFragmentById(R.id.welcomeFragment);
		
		// Initially, hide all fragments,  till the logic is run to set the correct one
		FragmentTransaction transaction = fm.beginTransaction();
		for(int fragmentIndex = 0; fragmentIndex< fragments.length;  fragmentIndex++){
			transaction.hide(fragments[fragmentIndex]);
		}
		
		Log.d(TAG, "onCreate: Hiding all Fragments");
		transaction.commit();
		
		String loginName = settings.getString(getResources().getString(R.string.pref_name_on_facebook),"");
		Boolean isAppSetupCompleted = settings.getBoolean(getResources().getString(R.string.pref_completed_app_setup),false);
		// Load the clubs list
		try {
			
			clubs = this.updateClubs();
			while( clubs == null){
				Log.e("Splash Activity","Waiting for Clubs List from Task");
				Thread.sleep(100);
			}
			db.open();
			Log.e("clubs", Integer.toString(clubs.size()));
			for(Club c: clubs){
				
				db.write(c);	
			}
			db.close();
			for(Club c: clubs){
				Log.e("Club",c.getName());
			}
			
			
			
			Bundle b = new Bundle();
			b.putParcelableArrayList("party.sense.app.clubsList", clubs);

			if (isAppSetupCompleted == false){
				// Go through Setup
				i = new Intent(this, SetupActivity.class);
				i.putExtras(b);
		    }else{
		    	// Go Directly to Main Activity
		    	i = new Intent(this, PartySenseMainActivity.class);
		    	i.putExtras(b);
		    }
			
			
			
		} catch(IOException exception){
			Log.e(TAG, exception.getMessage());
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		}
		int c = 0;
		for (int i = 0; i < FragmentGenreSetUp.genres.size(); i++) {
	        if(settings.getBoolean(FragmentGenreSetUp.genres.get(i), false)){
	        	c++;
	        }
	    }
		
	  /*fm = getSupportFragmentManager();
    	FragmentTransaction ft = fm.beginTransaction();
    	
    	
		if(loginName != null){
			WelcomeFragment welcomeFragment = (WelcomeFragment) fm.findFragmentById(R.id.welcomeFragment);
			welcomeFragment.setClubsList(clubs);
		}
		else{
			FacebookLoginFragment facebookLoginFragment = (FacebookLoginFragment) fm.findFragmentById(R.id.facebookLoginFragment);
			facebookLoginFragment.setClubsList(clubs);
		}*/
		
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
	
	@Override
	public void onResume() {	
		Log.d(TAG, "onResume");
		super.onResume();
		uiHelper.onResume();
		isResumed = true;
	}
	
	@Override
	public void onPause() {
		Log.d(TAG, "onPause");
		super.onPause();
		uiHelper.onPause();
		isResumed = false;
	}
	
	@Override
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);
		uiHelper.onActivityResult(requestCode, resultCode, data);
	}
	
	@Override
	public void onDestroy(){
		super.onDestroy();
		uiHelper.onDestroy();
	}
	
	@Override
	protected void onSaveInstanceState(Bundle outState) {
		super.onSaveInstanceState(outState);
		uiHelper.onSaveInstanceState(outState);
	}
	
	private void onSessionStateChange(Session session, SessionState state, Exception exception) {
		Log.i(TAG, "onSessionStateChange: " + state.name());
		
		// Only make changes if the activity is visible
		if (isResumed) {
			FragmentManager manager = getSupportFragmentManager();
			// Get number of entries in back stack
			int backStackSize = manager.getBackStackEntryCount();
			// Clear the back stack
			for (int backStackIterator = 0; backStackIterator < backStackSize; backStackIterator++) {
				manager.popBackStack();
			}
			if (state.isOpened()) {
				
				Log.i(TAG, "isOpened: Calling show fragment");
				showFragment(WELCOME, false);
				splashTimerThread.start();
			} else if (state.isClosed()) {
				
				Log.i(TAG, "isClosed: Calling show fragment");
				showFragment(LOGIN, false);
			}
		}
	}
	
	private void showFragment(int fragmentIndex, boolean addToBackStack) {
		FragmentManager fm = getSupportFragmentManager();
		FragmentTransaction transaction = fm.beginTransaction();
		
		for (int fragmentIter = 0; fragmentIter < fragments.length; fragmentIter++) {
			if (fragmentIter == fragmentIndex) {
				transaction.show(fragments[fragmentIter]);
			}else {
				transaction.hide(fragments[fragmentIter]);
			}
		}
		if (addToBackStack){
			transaction.addToBackStack(null);
		}
			
		Log.i(TAG, "showFragment: Trying to commit");
		transaction.commit();
		
	}
	
	@Override
	protected void onResumeFragments() {
		super.onResumeFragments();
		Session session = Session.getActiveSession();
		
		if (session != null && session.isOpened()){
			Log.i(TAG, "Calling ShowFragments for Selection Screen: Session is not null and isOpened");
			showFragment(WELCOME, false);
		} else {
			Log.i(TAG, "Calling ShowFragments for SplashScreen: Session is not null and isOpened");
			showFragment(LOGIN, false);
		}
	}
	
	public void setSplashWelcomeTimerStatus( boolean status) {
		
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


