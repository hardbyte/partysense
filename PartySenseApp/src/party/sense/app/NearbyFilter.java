package party.sense.app;

import java.util.ArrayList;

import android.location.Location;

public class NearbyFilter implements IClubFilter {
	
	private ArrayList<Club> clubList = new ArrayList<Club>();
	private ArrayList<Club> filteredClubList = new ArrayList<Club>();
	private RecommendedFilter r;
	public NearbyFilter (ArrayList<Club> newClubList){
		clubList = newClubList;
		//r = new RecommendedFilter(clubList, genreList);
	}
	
	
	public ArrayList<Club> getFilteredClubList(Location l, double dist) {
		filteredClubList.clear();
		double d;
		for (Club c: clubList){
			d = c.distanceTo(l);
			if(d<dist){
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
