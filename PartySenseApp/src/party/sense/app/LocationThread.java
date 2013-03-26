package party.sense.app;

import android.app.Activity;
import android.content.Context;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;

public class LocationThread extends Thread{
	private static final int TIME_INTV = 1000 * 5; //5 Seconds
	Location gpsLoc, ntwLoc, bestLoc;
	LocationManager gpsManager,ntwManager;
	LocationListener gpsListener, ntwListener;
	
	public LocationThread(Activity ac){
		
		gpsManager = (LocationManager) ac.getSystemService(Context.LOCATION_SERVICE);
	    ntwManager = (LocationManager) ac.getSystemService(Context.LOCATION_SERVICE);
		
		gpsListener = new LocationListener() {
	    	
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
		
		ntwListener = new LocationListener() {
	    	
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
		    
		
	}
	
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
						}
						else if (ntwLoc == null){
							bestLoc = gpsLoc;
						}
					}
					else if(gpsLoc == null){
						bestLoc = ntwLoc;
					}
					else if (ntwLoc == null){
						bestLoc = gpsLoc;
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
						}
						else if(isNtwValid && !isGpsValid){
							bestLoc = ntwLoc;
						}
						else if(isNtwValid && isGpsValid){
							if(gpsLoc.getAccuracy() <= ntwLoc.getAccuracy()){
								bestLoc = gpsLoc;
							}
							else{
								bestLoc = ntwLoc;
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
	
	public Location getCurrentLocation(){
		return bestLoc;
	}

	
	public void requestUpdates(){
		gpsManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, TIME_INTV, 2, gpsListener);
		ntwManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, TIME_INTV, 2, ntwListener);
	}
	
	public void stopRequest(){
		gpsManager.removeUpdates(gpsListener);
	    ntwManager.removeUpdates(ntwListener);
	}
}

