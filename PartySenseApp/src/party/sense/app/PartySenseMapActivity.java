package party.sense.app;

import com.google.android.maps.GeoPoint;
import com.google.android.maps.MapActivity;
import com.google.android.maps.MapController;
import com.google.android.maps.MapView;

import android.os.Bundle;

public class PartySenseMapActivity extends MapActivity {

	/** Called when the activity is first created. */
	
	MapController mController;
	GeoPoint geoP;
	MapView mapV;
	
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.layout_club_map);
	    mapV = (MapView) findViewById(R.id.mapview);
	    mapV.displayZoomControls(false);
	    mapV.setBuiltInZoomControls(true);
	    
	    double lon = 174.767;
	    double lat = -36.8667;
	    
	    geoP = new GeoPoint((int)(lat * 1E6) , (int)(lon * 1E6 ));
	    
	    mController = mapV.getController();
	    mController.animateTo(geoP);
	    mController.setZoom(14);
	    
	}

	@Override
	protected boolean isRouteDisplayed() {
		// TODO Auto-generated method stub
		return false;
	}

}
