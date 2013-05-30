package party.sense.app;

import java.util.ArrayList;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class WelcomeFragment extends Fragment {
	
	public static final String TAG = "WelcomeFragment"; 
	View view;
	ArrayList<Club> clubs = new ArrayList<Club>();
	Intent i;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		view = inflater.inflate(R.layout.layout_welcome_fragment, container,false);
		
		/*Bundle b = new Bundle();
		b.putParcelableArrayList("party.sense.app.clubsList", clubs);
		i = new Intent(getActivity(), PartySenseMainActivity.class);
		i.putExtras(b);
		
		final Thread splashTimerThread = new Thread(){
			public void run(){
				try{
					int counter = 0;
					while(counter<1)
					{
						Thread.sleep(2000);
						counter += 1;
					}
				}
				catch(Exception e){
					Log.d(TAG, "Exception : " + e.getMessage());
				}
				finally{
					startActivity(i);
					getActivity().finish();
				}
			}
		};
		splashTimerThread.start();*/
		return view;
	}
	
	/**
	 * Setter method for setting the Clubs List
	 * @param clubs The ArrayList containing the clubs to be added
	 */
	public void setClubsList(ArrayList<Club> clubs){
		this.clubs = clubs;
	}
}
