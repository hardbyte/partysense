package party.sense.app;

import android.app.Activity;
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
	    // TODO Auto-generated method stub
    	
    	btnNext = (Button) findViewById(R.id.btnNext);
    	btnBack = (Button) findViewById(R.id.btnBack);
    	
    	btnNext.setOnClickListener(new View.OnClickListener() {
			
			public void onClick(View v) {
				// TODO Auto-generated method stub
				//Toast.makeText(getApplicationContext(), Integer.toString(pageID), Toast.LENGTH_LONG).show();
				if(pageID == 0){
					if(((FragmentLogIn)fragLogIn).isLoggedIn()){
						changeFragment(1);
					}
					else{
						Toast.makeText(getApplicationContext(), "Please Log In first", Toast.LENGTH_LONG).show();
					}
				}
				else if(pageID == 1){
					if(((FragmentGenreSetUp)fragGenre).writeGenre()){
						Toast.makeText(getApplicationContext(), "Selection Stored", Toast.LENGTH_LONG).show();
						changeFragment(2);
					}
					else{
						Toast.makeText(getApplicationContext(), "Please Choose Genres", Toast.LENGTH_LONG).show();
					}
				}
				else{}
				
			}
		});
    	
	}

	public void changeFragment(int i){
		if(i<2){
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
		case 0:	return fragLogIn;
		case 1: return fragGenre;
		case 2: return fragConfirm;
		}
		return null;
	}
	
}
