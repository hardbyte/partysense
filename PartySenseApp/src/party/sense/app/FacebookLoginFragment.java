package party.sense.app;

import java.util.ArrayList;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

public class FacebookLoginFragment extends Fragment{
	View view;
	Intent i;
	ArrayList<Club> clubs = new ArrayList<Club>();
	private String userName;

	/* (non-Javadoc)
	 * @see android.support.v4.app.Fragment#onCreateView(android.view.LayoutInflater, android.view.ViewGroup, android.os.Bundle)
	 */
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		view = inflater.inflate(R.layout.layout_facebook_login_fragment, container,false);
		/*Button b = (Button) view.findViewById(R.id.btnLogin);
		
		b.setOnClickListener(new View.OnClickListener() {
			
			public void onClick(View v) {

                // Handle FB Login Button logic here

                // Get user name from Facebook (not facebook ID)
                userName = "DEVA";

				Bundle b = new Bundle();
				b.putString("login_name", userName);
				b.putParcelableArrayList("party.sense.app.clubsList", clubs);
				i = new Intent(getActivity(), SetupActivity.class);
				i.putExtras(b);
				startActivity(i);
				getActivity().finish();
			}
		});
		*/
		return view;
	}

	public void setClubArr(ArrayList<Club> clubs){
		this.clubs = clubs;
	}

	public String getName(){
		return userName;
	}
}
