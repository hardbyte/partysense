package party.sense.app;

import java.util.ArrayList;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

public class WelcomeFragment extends Fragment {
	View view;
	ArrayList<Club> clubs = new ArrayList<Club>();
	Intent i;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		view = inflater.inflate(R.layout.layout_welcome_fragment, container,false);
		/*Toast.makeText(getActivity(), Integer.toString(clubs.size()) + " clubs loaded!", Toast.LENGTH_LONG).show();
		
		Bundle b = new Bundle();
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
	
	public void setClubArr(ArrayList<Club> clubs){
		this.clubs = clubs;
	}
}
