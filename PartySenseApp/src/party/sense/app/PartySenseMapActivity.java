package party.sense.app;

import java.util.ArrayList;
import java.util.List;

import com.facebook.Session.NewPermissionsRequest;
import com.google.android.maps.GeoPoint;
import com.google.android.maps.MapActivity;
import com.google.android.maps.MapController;
import com.google.android.maps.MapView;
import com.google.android.maps.Overlay;
import com.google.android.maps.OverlayItem;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Point;
import android.graphics.drawable.Drawable;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.widget.Toast;

public class PartySenseMapActivity extends MapActivity {

	/** Called when the activity is first created. */
	
	
	
	List<Overlay> mapOverlays;
	LocationManager lManager;
	GeoPoint geoP;
	MapView mapV;
	
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.layout_club_map);
	    mapV = (MapView) findViewById(R.id.mapview);
	    lManager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);
	    final MapController mController = mapV.getController();
	    mapV.displayZoomControls(true);
	    mapV.setBuiltInZoomControls(true);
	    
	    
	    mapOverlays = mapV.getOverlays();
	    Drawable pinDraw = this.getResources().getDrawable(R.drawable.pin_0);
	    int w = pinDraw.getIntrinsicWidth();
		int h = pinDraw.getIntrinsicHeight();
		pinDraw.setBounds(-w / 50, -h, w / 50, 0);
	    final MyLocationItem myLocItemOverlay = new MyLocationItem(pinDraw, this);
	    LocationListener locListener = new LocationListener() {
			
			public void onStatusChanged(String provider, int status, Bundle extras) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProviderEnabled(String provider) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProviderDisabled(String provider) {
				// TODO Auto-generated method stub
				
			}
			
			public void onLocationChanged(Location location) {
				// TODO Auto-generated method stub
				//mController.animateTo(geoP);
				GeoPoint point = new GeoPoint((int)(location.getLatitude() * 1E6), (int) (location.getLongitude() * 1E6));
				
				//Toast.makeText(getApplicationContext(), "123", duration)
				
				OverlayItem overlayitem = new OverlayItem(point, "", "");
				//mController.setCenter(point);
				myLocItemOverlay.clear();
				myLocItemOverlay.addOverlay(overlayitem);
			}
		};
	    
		lManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 5000, 2, locListener);
		mapOverlays.add(myLocItemOverlay);
	    
	    /*double lon = 174.767;
	    double lat = -36.8667;
	    
	    geoP = new GeoPoint((int)(lat * 1E6) , (int)(lon * 1E6 ));
	    
	    mController = mapV.getController();
	    mController.animateTo(geoP);
	    mController.setZoom(14);*/
	    
	}

	@Override
	protected boolean isRouteDisplayed() {
		// TODO Auto-generated method stub
		return false;
	}
	
	
	
	
	

}
