/**
 * 
 */
package party.sense.app;

import android.app.Activity;
import android.content.Intent;
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
 * @author Tanmay Bhola [tanmay9@gmail.com] 
 *
 */
public class PartySenseLoginActivity extends Activity {
	
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.layout_login_screen);
		
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
	
	public boolean loginViaFacebook(){
		Session.openActiveSession(this, true, new Session.StatusCallback() {
			
			public void call(Session session, SessionState state, Exception exception) {
				if (session.isOpened()){
					Request.executeMeRequestAsync(session, new Request.GraphUserCallback() {
						
						public void onCompleted(GraphUser user, Response response) {
							if (user != null){
								TextView loggedInUser = (TextView)findViewById(R.id.textViewLoggedInUser);
								Toast.makeText(getApplicationContext(), "Succesfully Logged in", Toast.LENGTH_SHORT).show();
								loggedInUser.setText(user.getName());
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
