package party.sense.app;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class PartySenseDetailsActivity extends Activity {
	public static final String BUNDLE_ID_CLUB_NAME = "ClubName";
	public static final String BUNDLE_ID_CLUB_GENRE = "ClubGenre";
	public static final String BUNDLE_ID_CLUB_ADDRESS = "ClubAddress";
	public static final String BUNDLE_ID_CLUB_WEBSITE = "ClubWebsite";
	public static final String BUNDLE_ID_CLUB_DESCRIPTION = "ClubDescription";
	
	TextView tvClubName, tvClubAddress, tvClubGenres, tvClubDescription;
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.layout_club_details);
	    
	    tvClubName = (TextView) findViewById(R.id.txtClubName);
	    tvClubGenres = (TextView) findViewById(R.id.txtGenre);
	    tvClubAddress = (TextView) findViewById(R.id.txtStreetAddress);
	    tvClubDescription = (TextView) findViewById(R.id.txtDescription);
	    
	    String clubName = getIntent().getExtras().getString("ClubName");
	    
	    tvClubName.setText(getIntent().getExtras().getString(PartySenseDetailsActivity.BUNDLE_ID_CLUB_NAME));
	    tvClubGenres.setText(getIntent().getExtras().getString(PartySenseDetailsActivity.BUNDLE_ID_CLUB_GENRE));
	    tvClubAddress.setText(getIntent().getExtras().getString(PartySenseDetailsActivity.BUNDLE_ID_CLUB_ADDRESS));
	    tvClubDescription.setText(getIntent().getExtras().getString(PartySenseDetailsActivity.BUNDLE_ID_CLUB_DESCRIPTION));
	    // TODO Auto-generated method stub
	}

}
