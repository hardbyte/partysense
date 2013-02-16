package party.sense.app;

import java.util.ArrayList;

import android.location.Location;

public class NearbyFilter implements IClubFilter {
	
	private ArrayList<Club> clubList = new ArrayList<Club>();
	private ArrayList<Club> filteredClubList = new ArrayList<Club>();
	private int maxDistanceMeters;
	Location l = new Location("a");
	public NearbyFilter (ArrayList<Club> newClubList, int maxDistMeters){
		clubList = newClubList;
		maxDistanceMeters = maxDistMeters;
	}
	
	public void setMaxDistMeters(int maxDistMeters){
		maxDistanceMeters = maxDistMeters;
	}
	
	public ArrayList<Club> getFilteredClubList(double lat, double lon) {
		l.setLatitude(lat);
		l.setLongitude(lon);
		float dist;
		filteredClubList.clear();
		for (Club c: clubList){
			dist = l.distanceTo(c.getLocation());
			if (Math.round(dist) < maxDistanceMeters){
				filteredClubList.add(c);
			}
		}
		return filteredClubList;
	}

	public void setClubList(ArrayList<Club> newClubList) {
		clubList = newClubList;
	}

	public void addClub(Club newClub) {
		clubList.add(newClub);
	}

}
