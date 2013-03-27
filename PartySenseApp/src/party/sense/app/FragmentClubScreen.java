package party.sense.app;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import com.google.android.maps.GeoPoint;
import com.google.android.maps.OverlayItem;

import android.R.integer;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.Toast;

public class FragmentClubScreen extends Fragment {
	ArrayList<ClubListItem> clubListArray = new ArrayList<ClubListItem>();
	ListView lvClubList;
	Button btnTest, switch1;
	LocationManager gpsManager,ntwManager;
	private static final int TIME_INTV = 1000 * 5; //5 Seconds
	Location bestLoc = null;
	Location gpsLoc = null;
	Location ntwLoc = null;
	volatile boolean locationThreadFlag = false;
	LocationListener gpsListener, ntwListener;
	ArrayList<Club> clubsList;
	
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
		
	};
	
	
	//LocationThread locThd;
	//Switch switch1;
	ClubListItemAdapter adapter;
	View view;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		
		view = inflater.inflate(R.layout.layout_club_screen, container,false);
		//edtView.setInputType(0);
		Bundle b = this.getArguments();
		clubsList = b.getParcelableArrayList("party.sense.app.clubsList");
		lvClubList = (ListView) view.findViewById(R.id.nearby_club_listview);
		btnTest = (Button) view.findViewById(R.id.btnTest);
		//locThd = new LocationThread(this.getActivity());
		
		gpsManager = (LocationManager) this.getActivity().getSystemService(Context.LOCATION_SERVICE);
	    ntwManager = (LocationManager) this.getActivity().getSystemService(Context.LOCATION_SERVICE);
		
		btnTest.setOnClickListener(new OnClickListener() {
			public void onClick(View v) {
				if(bestLoc!=null){
					Date date = new Date(bestLoc.getTime());
					SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
					String myDate= sdf.format(date);
					Toast.makeText(getActivity(), myDate, Toast.LENGTH_LONG).show();
					clubListArray.clear();
					for(Club c: clubsList){
						addClubItem(c,bestLoc);
					}
				}
				else{
					Toast.makeText(getActivity(), "Please wait, getting location data", Toast.LENGTH_LONG).show();
				}	
			}
		});
		
		
		
		clubListArray.add(new ClubListItem(R.color.transparent, "Waiting for location","Press update in a few seconds"));
		
		adapter = new ClubListItemAdapter(getActivity(), R.layout.club_item, clubListArray);
		
		lvClubList.setAdapter(adapter);
		
		lvClubList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			public void onItemClick(AdapterView<?> adapterView, View view, int pos, long id) {
	            /*if (pos == adapter.getCount()-1){
	            	//startActivity(new Intent("android.intent.action.PartySenseMainActivity"));
	            	adapter.removeLast();
	            	addClubItem(R.drawable.item_bg, "ClubTanmay", "HipHop/Bhangra");
	            	addClubItem(R.color.blue_rect, "Load more Clubs", "");
	            }
	            else{
	            	
	            	Intent detailIntent = new Intent("android.intent.action.PartySenseDetailsActivity");
	            	detailIntent.putExtra("ClubName", adapter.getItem(pos).ClubName);
	            	startActivity(detailIntent);
	            }*/
            }
		});
		
		//addClubItem(R.color.blue_rect, "Load more Clubs", "");
		
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
		
		return view;
	}
	
	public void onPause() {
	    super.onPause();  // Always call the superclass method first
	    /*locThd.stopRequest();
	    locThd.stop();*/
	    
	    gpsManager.removeUpdates(gpsListener);
	    ntwManager.removeUpdates(ntwListener);
	    //locationThread.stop();
	}
	
	@Override
	public void onResume() {
	    super.onResume();
	    /*locThd.requestUpdates();
	    locThd.start();*/
	    
	    gpsManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, TIME_INTV, 2, gpsListener);
		ntwManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, TIME_INTV, 2, ntwListener);
		if(!locationThread.isAlive()){
			locationThread.start();
		}
	}
	
	
	private void addClubItem(int imgID, String clubName, String clubSub){
		adapter.add(new ClubListItem(imgID, clubName, clubSub));
	}
	
	private void addClubItem(Club c, Location bst){
		
		adapter.add(new ClubListItem(R.drawable.item_bg, c.getName(),String.format("%.2fkm", c.distanceTo(bst))));	
	}
	
	
	
	
}
