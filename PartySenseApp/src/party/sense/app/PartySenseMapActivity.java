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
import android.location.Criteria;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.widget.Toast;

public class PartySenseMapActivity extends MapActivity {

	/** Called when the activity is first created. */
	
	
	
	
	
	List<Overlay> mapOverlays;
	LocationManager gpsManager,ntwManager;
	GeoPoint geoP;
	MapView mapV;
	private static final int TIME_INTV = 1000 * 5; //5 Seconds
	Location bestLoc = null;
	Location gpsLoc = null;
	Location ntwLoc = null;
	volatile boolean locationThreadFlag = false;
	
	
	//pinDraw.setBounds(-w / 50, -h, w / 50, 0);
    MyLocationItem myLocItemOverlay;
    
	final Thread locationThread = new Thread(){
		public void run(){
			try{
				long dGpsTime = -50;
				long dNtwTime = -50;
				boolean isGpsValid = false;
				boolean isNtwValid = false;
				while(true){	
					
					if((gpsLoc == null) && (ntwLoc == null)){
						
					}
					else{
						if(bestLoc == null){
							if(gpsLoc == null){
								bestLoc = ntwLoc;
								draw();
							}
							else if (ntwLoc == null){
								bestLoc = gpsLoc;
								draw();
							}
						}
						else if(gpsLoc == null){
							bestLoc = ntwLoc;
							draw();
						}
						else if (ntwLoc == null){
							bestLoc = gpsLoc;
							draw();
						}
						else{
							dGpsTime = gpsLoc.getTime() - bestLoc.getTime();
							if (dGpsTime > 0){
								isGpsValid = true;
							}
							else{
								isGpsValid = false;
							}
							dNtwTime = ntwLoc.getTime() - bestLoc.getTime();
							if (dNtwTime > 0){
								isNtwValid = true;
							}
							else{
								isNtwValid = false;
							}
							if(isGpsValid && !isNtwValid){
								bestLoc = gpsLoc;
								draw();
							}
							else if(isNtwValid && !isGpsValid){
								bestLoc = ntwLoc;
								draw();
							}
							else if(isNtwValid && isGpsValid){
								if(gpsLoc.getAccuracy() <= ntwLoc.getAccuracy()){
									bestLoc = gpsLoc;
									draw();
								}
								else{
									bestLoc = ntwLoc;
									draw();
								}
							}
							else{
								
							}
							
						}
					}
					Thread.sleep(3000);
				}
			}
			catch(Exception e){
			}
			finally{
			}
		}
		
		public void draw(){
			myLocItemOverlay.clear();
			
			for(int i = 0; i<10;i++){
				GeoPoint point = new GeoPoint((int)(bestLoc.getLatitude() * 1E6+(i*500)), (int) (bestLoc.getLongitude() * 1E6+(i*500)));
				OverlayItem overlayitem = new OverlayItem(point, "", "");
				myLocItemOverlay.addOverlay(overlayitem);
			}
			
			mapV.postInvalidate();
		}
	};
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.layout_club_map);
	    mapV = (MapView) findViewById(R.id.mapview);
	    gpsManager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);
	    ntwManager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);
	    final MapController mController = mapV.getController();
	    mapV.displayZoomControls(true);
	    mapV.setBuiltInZoomControls(true);
	    Drawable pinDraw = this.getResources().getDrawable(R.drawable.pin_0);
	    int w = pinDraw.getIntrinsicWidth();
		int h = pinDraw.getIntrinsicHeight();
	    pinDraw.setBounds(-w / 50, -h, w / 50, 0);
	    myLocItemOverlay = new MyLocationItem(pinDraw, this);
	    mapOverlays = mapV.getOverlays();
	    
	    LocationListener gpsListener = new LocationListener() {
	    	
			public void onStatusChanged(String provider, int status, Bundle extras) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProviderEnabled(String provider) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProviderDisabled(String provider) {
				//Toast.makeText(getApplicationContext(), "Please turn GPS on", Toast.LENGTH_LONG).show();
			}
			
			public void onLocationChanged(Location location) {
				// TODO Auto-generated method stub
				//mController.animateTo(geoP);
				/*GeoPoint point = new GeoPoint((int)(location.getLatitude() * 1E6), (int) (location.getLongitude() * 1E6));
				
				
				OverlayItem overlayitem = new OverlayItem(point, "", "");
				//mController.setCenter(point);
				myLocItemOverlay.clear();
				myLocItemOverlay.addOverlay(overlayitem);*/
				
				/*if(!gpsManager.isProviderEnabled(LocationManager.NETWORK_PROVIDER)){
					bestLoc = location;
					Toast.makeText(getApplicationContext(), "GPS:\n" + location.getLatitude() + "\n" + location.getLongitude() + "\n" + location.getAccuracy(), Toast.LENGTH_LONG).show();
				}
				else if(isBetterLocation(location, bestLoc)){
					bestLoc = location;
					Toast.makeText(getApplicationContext(), "GPS:\n" + location.getLatitude() + "\n" + location.getLongitude() + "\n" + location.getAccuracy(), Toast.LENGTH_LONG).show();
				}
				else{
					
				}
				GeoPoint point = new GeoPoint((int)(bestLoc.getLatitude() * 1E6), (int) (bestLoc.getLongitude() * 1E6));
				OverlayItem overlayitem = new OverlayItem(point, "", "");
				
				myLocItemOverlay.clear();
				myLocItemOverlay.addOverlay(overlayitem);*/
				
				gpsLoc = location;
				//Toast.makeText(getApplicationContext(), "GPS Location", Toast.LENGTH_LONG).show();
				
			}
		};
		
		LocationListener ntwListener = new LocationListener() {
	    	
			public void onStatusChanged(String provider, int status, Bundle extras) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProviderEnabled(String provider) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProviderDisabled(String provider) {
				//Toast.makeText(getApplicationContext(), "Please turn GPS on", Toast.LENGTH_LONG).show();
			}
			
			public void onLocationChanged(Location location) {
				// TODO Auto-generated method stub
				//mController.animateTo(geoP);
				/*GeoPoint point = new GeoPoint((int)(location.getLatitude() * 1E6), (int) (location.getLongitude() * 1E6));
				
				
				OverlayItem overlayitem = new OverlayItem(point, "", "");
				//mController.setCenter(point);
				myLocItemOverlay.clear();
				myLocItemOverlay.addOverlay(overlayitem);
				if(!gpsManager.isProviderEnabled(LocationManager.GPS_PROVIDER)){
					bestLoc = location;
					Toast.makeText(getApplicationContext(), "Network:\n" + location.getLatitude() + "\n" + location.getLongitude() + "\n" + location.getAccuracy(), Toast.LENGTH_LONG).show();
				}
				else if(isBetterLocation(location, bestLoc)){
					bestLoc = location;
					Toast.makeText(getApplicationContext(), "Network:\n" + location.getLatitude() + "\n" + location.getLongitude() + "\n" + location.getAccuracy(), Toast.LENGTH_LONG).show();
				}
				else{
					
				}
				
				GeoPoint point = new GeoPoint((int)(bestLoc.getLatitude() * 1E6), (int) (bestLoc.getLongitude() * 1E6));
				OverlayItem overlayitem = new OverlayItem(point, "", "");
				
				myLocItemOverlay.clear();
				myLocItemOverlay.addOverlay(overlayitem);*/
				ntwLoc = location;
			}
		};

		
		gpsManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, TIME_INTV, 2, gpsListener);
		ntwManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, TIME_INTV, 2, ntwListener);
		mapOverlays.add(myLocItemOverlay);
		
		
		locationThread.start();
		
		
	}

	
	protected boolean isBetterLocation(Location location, Location currentBestLocation) {
	    if (currentBestLocation == null) {
	        // A new location is always better than no location
	        return true;
	    }

	    // Check whether the new location fix is newer or older
	    long timeDelta = location.getTime() - currentBestLocation.getTime();
	    boolean isSignificantlyNewer = timeDelta > TIME_INTV;
	    boolean isSignificantlyOlder = timeDelta < -TIME_INTV*2;
	    boolean isNewer = timeDelta > 0;

	    // If it's been more than two minutes since the current location, use the new location
	    // because the user has likely moved
	    if (isSignificantlyNewer) {
	        return true;
	    // If the new location is more than two minutes older, it must be worse
	    } else if (isSignificantlyOlder) {
	        return false;
	    }

	    // Check whether the new location fix is more or less accurate
	    int accuracyDelta = (int) (location.getAccuracy() - currentBestLocation.getAccuracy());
	    boolean isLessAccurate = accuracyDelta > 0;
	    boolean isMoreAccurate = accuracyDelta < 0;
	    boolean isSignificantlyLessAccurate = accuracyDelta > 200;

	    // Check if the old and new location are from the same provider
	    boolean isFromSameProvider = isSameProvider(location.getProvider(),
	            currentBestLocation.getProvider());

	    // Determine location quality using a combination of timeliness and accuracy
	    if (isMoreAccurate) {
	        return true;
	    } else if (isNewer && !isLessAccurate) {
	        return true;
	    } else if (isNewer && !isSignificantlyLessAccurate && isFromSameProvider) {
	        return true;
	    }
	    return false;
	}
	
	/** Checks whether two providers are the same */
	private boolean isSameProvider(String provider1, String provider2) {
	    if (provider1 == null) {
	      return provider2 == null;
	    }
	    return provider1.equals(provider2);
	}
	
	@Override
	protected boolean isRouteDisplayed() {
		// TODO Auto-generated method stub
		return false;
	}
	
	
	
	
	

}
