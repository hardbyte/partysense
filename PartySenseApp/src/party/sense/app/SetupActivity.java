package party.sense.app;

import java.util.ArrayList;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class SetupActivity extends FragmentActivity {

	static FragmentManager fm;
	static int pageID = 0;
	static Fragment fragLogIn = new FragmentLogIn();
	static Fragment fragGenre = new FragmentGenreSetUp();
	static Fragment fragConfirm = new FragSetupConfim();
	Button btnNext;
	Button btnBack;
	ArrayList<Club> clubs = new ArrayList<Club>();
	ArrayList<Boolean> selectionValues = new ArrayList<Boolean>();
	SharedPreferences settings;
	SharedPreferences.Editor edit;
	ArrayList<String> genres = new ArrayList<String>();
	String userName = "";
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
        setContentView(R.layout.layout_setup);
        pageID = 0;
    	fm = getSupportFragmentManager();
    	FragmentTransaction ft = fm.beginTransaction();
    	ft.add(R.id.fragSetUp, getFragment(pageID));
    	ft.commit();
	    
    	settings = getSharedPreferences(SplashActivity.PREFS_NAME, 0);
	    edit = settings.edit();
	    
	    // TODO Remove this : Temporary declaration 
	    userName = "Tanmay";
	    edit.putString(getResources().getString(R.string.pref_name_on_facebook), userName);
	    edit.commit();
    	
    	Bundle b = getIntent().getExtras();
    	//this.userName = b.getString("login_name");
        //this.clubs = b.getParcelableArrayList("party.sense.app.clubsList");
    	
    	btnNext = (Button) findViewById(R.id.btnNext);
    	btnBack = (Button) findViewById(R.id.btnBack);
    	
    	btnNext.setOnClickListener(new View.OnClickListener() {
			
			public void onClick(View v) {
				//Toast.makeText(getApplicationContext(), Integer.toString(pageID), Toast.LENGTH_LONG).show();
				if(pageID == 0){
					selectionValues = ((FragmentGenreSetUp)fragGenre).genresSelected();
					if(selectionValues.size()>0){
						Toast.makeText(getApplicationContext(), "Selection Stored", Toast.LENGTH_LONG).show();
						changeFragment(1);
					}
					else{
						Toast.makeText(getApplicationContext(), "Please Choose Genres", Toast.LENGTH_LONG).show();
					}
				}
				else if (pageID == 1){
					genres = FragmentGenreSetUp.genres;
					for (int i = 0; i < selectionValues.size(); i++) {
				        edit.putBoolean(genres.get(i), selectionValues.get(i));
				    }
					edit.putBoolean(getResources().getString(R.string.pref_completed_app_setup), true);
					edit.commit();
					
					Bundle b = new Bundle();
					b.putParcelableArrayList("party.sense.app.clubsList", clubs);
					Intent i = new Intent(getApplicationContext(), PartySenseMainActivity.class);
					i.putExtras(b);
					startActivity(i);
					finish();
					Toast.makeText(getApplicationContext(), userName, Toast.LENGTH_SHORT).show();
				}
				else{
					
				}
				
			}
		});
    	
	}

	public void changeFragment(int i){
		if(i<1){
			btnNext.setText("Next");
		}
		else{
			btnNext.setText("Finish");
		}
		FragmentTransaction ft = fm.beginTransaction();
		ft.replace(R.id.fragSetUp, getFragment(i));
		ft.setTransition(FragmentTransaction.TRANSIT_NONE);
		ft.commit();
		pageID = i;
		Log.d("Fragement", "WORKING");
	}
	
	private Fragment getFragment(int i){
		switch (i){
		case 0: return fragGenre;
		case 1: return fragConfirm;
		}
		return null;
	}
	
}
