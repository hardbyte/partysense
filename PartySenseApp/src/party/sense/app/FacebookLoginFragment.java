package party.sense.app;

import java.util.ArrayList;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

/**
 * Fragment showing the Facebook Login Button on the splash screen
 * @author Tanmay Bhola [tanmay9@gmail.com]
 *
 */
public class FacebookLoginFragment extends Fragment{
	
	public static final String TAG = "FacebookLoginFragment";
	
	View view;
	Intent i;
	ArrayList<Club> clubs = new ArrayList<Club>();
	private String facebookUserName;

	/* (non-Javadoc)
	 * @see android.support.v4.app.Fragment#onCreateView(android.view.LayoutInflater, android.view.ViewGroup, android.os.Bundle)
	 */
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		Log.d(TAG, "onCreateView");
		view = inflater.inflate(R.layout.layout_facebook_login_fragment, container,false);
		return view;
	}

	/**
	 * Setter method for setting the Clubs List
	 * @param clubs The ArrayList containing the clubs to be added
	 */
	public void setClubsList(ArrayList<Club> clubs){
		this.clubs = clubs;
	}

	/**
	 * Getter method for returning User's facebook name 
	 * @return String containing the users facebook name
	 */
	public String getFacebookUserName(){
		return facebookUserName;
	}
}
