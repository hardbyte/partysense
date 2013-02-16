package party.sense.app;

import java.util.ArrayList;
import org.apache.http.message.BasicNameValuePair;
import android.content.SharedPreferences;

public class RecommendedFilter implements IClubFilter {
 
	private ArrayList<Club> clubList = new ArrayList<Club>();
	
	public RecommendedFilter(ArrayList<Club> newClubList, ArrayList<String> genreSelectionList)
	{
		for(Club c : newClubList){
			for(String s : genreSelectionList){
				if(c.getGenres().contains(s.toUpperCase())){
					clubList.add(c);
					break;
				}
			}
		}
	}
	
	public ArrayList<Club> getFilteredClubList() 
	{
		// TODO Auto-generated method stub
		return clubList;
	}

	public void setClubList(ArrayList<Club> newClubList) 
	{
		clubList = newClubList;
	}

	public void addClub(Club newClub) 
	{
		clubList.add(newClub);
		
	}

}
