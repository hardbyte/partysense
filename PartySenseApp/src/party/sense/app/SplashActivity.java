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

import com.facebook.Session;
import com.facebook.SessionState;
import com.facebook.UiLifecycleHelper;

public class SplashActivity extends FragmentActivity {
	
	SharedPreferences settings;
	private static final String TAG = "SplashActivity";
	public static final String BUNDLE_ID_CLUBS_LIST = "party.sense.app.clubsList";
	
	private static final int LOGIN = 0;
	private static final int WELCOME = 1;
	private static final int FRAGMENT_COUNT = WELCOME + 1;
	private Fragment[] fragments = new Fragment[FRAGMENT_COUNT];
	
	private boolean isResumed = false;
	
	private UiLifecycleHelper uiHelper;
	private Session.StatusCallback callback = new Session.StatusCallback() {

		public void call(Session session, SessionState state, Exception exception) {
			onSessionStateChange(session, state, exception);
		}
	};
	
	Intent i;
	Button btnLogin;
	TextView txtLogin;
	
	FragmentManager fm;
	
	/** Called when the activity is first created. */
	@Override

	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.layout_splash_activity);
		ArrayList<Club> clubs = new ArrayList<Club>();
		settings = getSharedPreferences(FragmentMenuScreen.PREFS_NAME, 0);
		
		uiHelper = new UiLifecycleHelper(this, callback);
		uiHelper.onCreate(savedInstanceState);
		FragmentManager fm = getSupportFragmentManager();
		fragments[LOGIN] = fm.findFragmentById(R.id.facebookLoginFragment);
		fragments[WELCOME] = fm.findFragmentById(R.id.welcomeFragment);
		
		FragmentTransaction transaction = fm.beginTransaction();
		for(int i = 0; i< fragments.length;  i++){
			transaction.hide(fragments[i]);
		}
		
		Log.d(TAG, "onCreate: Hiding all Fragments");
		transaction.commit();
		
		//String loginName = settings.getString(getResources().getString(R.string.pref_name_on_facebook),null);
		
		/*
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
			

		} catch(IOException exception){
			Log.e(TAG, exception.getMessage());
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		}
	  */
		
	  /*fm = getSupportFragmentManager();
    	FragmentTransaction ft = fm.beginTransaction();
    	
    	
		if(loginName != null){
			((FragSplashLogged)fragWelcom).setClubArr(clubs);
			ft.add(R.id.fragLoginLayout, fragWelcom);
		}
		else{
			((FacebookLoginFragment)fragLogin).setClubArr(clubs);
			ft.add(R.id.fragLoginLayout, fragLogin);
		}
		
		ft.commit();*/
		

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
			for (int i = 0; i < backStackSize; i++) {
				manager.popBackStack();
			}
			if (state.isOpened()) {
				
				Log.i(TAG, "isOpened: Calling show fragment");
				showFragment(WELCOME, false);
			} else if (state.isClosed()) {
				
				Log.i(TAG, "isClosed: Calling show fragment");
				showFragment(LOGIN, false);
			}
		}
	}
	
	private void showFragment(int fragmentIndex, boolean addToBackStack) {
		FragmentManager fm = getSupportFragmentManager();
		FragmentTransaction transaction = fm.beginTransaction();
		
		for (int i = 0; i < fragments.length; i++) {
			if (i == fragmentIndex) {
				transaction.show(fragments[i]);
			}else {
				transaction.hide(fragments[i]);
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


