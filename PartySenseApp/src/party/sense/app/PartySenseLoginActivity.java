/**
 * 
 */
package party.sense.app;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.facebook.Request;
import com.facebook.Response;
import com.facebook.Session;
import com.facebook.SessionState;
import com.facebook.model.GraphUser;

/**
 * Activity to handle User Login into PartySense
 * @author Tanmay Bhola [tanmay9@gmail.com] 
 *
 */
public class PartySenseLoginActivity extends Activity {
	
	SharedPreferences settings;
	SharedPreferences.Editor edit;
	
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.layout_login_screen);
		
		settings = getSharedPreferences(FragmentMenuScreen.PREFS_NAME, 0);
	    edit = settings.edit();
	    
		ImageView facebookLoginButton = (ImageView)findViewById(R.id.imageView_login_facebook);
		facebookLoginButton.setOnClickListener(new OnClickListener() {
			
			public void onClick(View v) {
				Toast.makeText(getApplicationContext(), "Facebook Login", Toast.LENGTH_SHORT).show();
				loginViaFacebook();
			}
		});
	}
	
	@Override
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
	  super.onActivityResult(requestCode, resultCode, data);
	  Session.getActiveSession().onActivityResult(this, requestCode, resultCode, data);
	}
	
	/**
	 * Method containing Facebook's login logic
	 * @return True if the user was successfully logged in
	 */
	public boolean loginViaFacebook(){
		Session.openActiveSession(this, true, new Session.StatusCallback() {
			
			public void call(Session session, SessionState state, Exception exception) {
				if (session.isOpened()){
					Request.executeMeRequestAsync(session, new Request.GraphUserCallback() {
						
						public void onCompleted(GraphUser user, Response response) {
							if (user != null){
								TextView loggedInUser = (TextView)findViewById(R.id.textViewLoggedInUser);
								Toast.makeText(getApplicationContext(), "Succesfully Logged in", Toast.LENGTH_SHORT).show();
								String nameOnFacebook = user.getName();
								loggedInUser.setText(nameOnFacebook);
								// Add the name to Shared Preferences
								edit.putString(getResources().getString(R.string.pref_name_on_facebook), nameOnFacebook);
								// TODO Should update login infomation in the Backend at this stage (number of online users)
							}
						}
					});
				}
			}
		});
		return true;
	}
	
	
	
}
