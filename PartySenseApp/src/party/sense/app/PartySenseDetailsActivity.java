package party.sense.app;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class PartySenseDetailsActivity extends Activity {

	TextView tvClubName;
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.layout_club_details);
	    
	    tvClubName = (TextView) findViewById(R.id.txtClubName);
	    
	    String clubName = getIntent().getExtras().getString("ClubName");
	    tvClubName.setText(clubName);
	    
	    // TODO Auto-generated method stub
	}

}
