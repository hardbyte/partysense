package party.sense.app;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

public class FragFBLogin extends Fragment{
	View view;
	SharedPreferences settings;
	SharedPreferences.Editor edit;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		view = inflater.inflate(R.layout.frag_fb_login, container,false);
		Button b = (Button) view.findViewById(R.id.tstButton);
		settings = getActivity().getSharedPreferences(FragmentMenuScreen.PREFS_NAME, 0);
	    edit = settings.edit();
	    edit.putString(getResources().getString(R.string.pref_name_on_facebook), "DEVA");
		edit.commit();
		
		return view;
	}
}
