package party.sense.app;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class FragmentLogIn extends Fragment {
	SharedPreferences settings;
	SharedPreferences.Editor edit;
	View view;
	String loginName = "";
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		view = inflater.inflate(R.layout.layout_setup_fragment, container,false);
		TextView tv = (TextView) view.findViewById(R.id.tvMsg);
		final EditText txtLogin = (EditText) view.findViewById(R.id.txtLogin);
		Button b = (Button) view.findViewById(R.id.tstButton);
		settings = getActivity().getSharedPreferences(FragmentMenuScreen.PREFS_NAME, 0);
	    edit = settings.edit();
	    loginName = settings.getString("login_name", "");
	    if (loginName == ""){
	    	tv.setText("You are not logged in");
	    }
	    else{
	    	tv.setText("You are logged in as " + loginName);
	    	txtLogin.setText(loginName);
	    }
		b.setOnClickListener(new View.OnClickListener() {
			
			public void onClick(View v) {
				//Toast.makeText(getActivity(), "DEVA",Toast.LENGTH_LONG).show();
				loginName = txtLogin.getText().toString();
				edit.putString("login_name", loginName);
				edit.commit();
			}
		}); 
		return view;
	}
	
	public boolean isLoggedIn(){
		return loginName!="";
	}
	
}
