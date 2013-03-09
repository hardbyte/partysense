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
	
	double[] lats = {-43.518245,-43.517871,-43.515444,-43.518929,-43.524157,-43.526398,-43.52926,-43.527518,-43.502869,-43.539776};
	double[] lons = {172.583885,172.580023,172.569551,172.568521,172.57453,172.566633,172.571611,172.578478,172.571096,172.599421};
	
	ArrayList<Location> locList = new ArrayList<Location>();
	
	//pinDraw.setBounds(-w / 50, -h, w / 50, 0);
    MyLocationItem myLocItemOverlay;
    MyLocationItem clubLocItemOverlay;
    
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
			clubLocItemOverlay.clear();
			GeoPoint point = new GeoPoint((int)(bestLoc.getLatitude() * 1E6), (int) (bestLoc.getLongitude() * 1E6));
			OverlayItem overlayitem = new OverlayItem(point, "", "");
			myLocItemOverlay.addOverlay(overlayitem);
			double d;
			for(Location l:locList){
				d = distanceTo(l, bestLoc);
				
				if(d<1){
					point = new GeoPoint((int)(l.getLatitude() * 1E6), (int) (l.getLongitude() * 1E6));
					overlayitem = new OverlayItem(point, "Distance:", Double.toString(d));
					clubLocItemOverlay.addOverlay(overlayitem);
				}
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
	    Drawable clubDraw = this.getResources().getDrawable(R.drawable.pin_1);
	    int w = pinDraw.getIntrinsicWidth();
		int h = pinDraw.getIntrinsicHeight();
	    pinDraw.setBounds(-w / 50, -h, w / 50, 0);
	    clubDraw.setBounds(-w / 50, -h, w / 50, 0);
	    myLocItemOverlay = new MyLocationItem(pinDraw, this);
	    clubLocItemOverlay = new MyLocationItem(clubDraw, this);
	    mapOverlays = mapV.getOverlays();
	    Location loc;
	    for(int b = 0; b<lats.length; b++){
	    	loc = new Location("a");
			loc.setLatitude(lats[b]);
			loc.setLongitude(lons[b]);
			locList.add(loc);
	    }
	    
	    
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
				ntwLoc = location;
			}
		};

		gpsManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, TIME_INTV, 2, gpsListener);
		ntwManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, TIME_INTV, 2, ntwListener);
		mapOverlays.add(myLocItemOverlay);
		mapOverlays.add(clubLocItemOverlay);

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
	
	public double distanceTo(Location thatLoc, Location thisLoc){
		//Algorithm from    http://www.movable-type.co.uk/scripts/latlong.html
		double R = 6371.0; // km
		
		double dLat = Math.toRadians(thisLoc.getLatitude() - thatLoc.getLatitude());
		double dLon = Math.toRadians(thisLoc.getLongitude() - thatLoc.getLongitude());
		
		double lat1 = Math.toRadians(thatLoc.getLatitude());
		double lat2 = Math.toRadians(thisLoc.getLatitude());

		double a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
		double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
		double d =  R * c;
		return d;
	}
	
	
	

}
