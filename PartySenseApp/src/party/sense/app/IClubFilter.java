package party.sense.app;

import java.util.ArrayList;
import java.util.Dictionary;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Map;

import org.apache.http.message.BasicNameValuePair;

public interface IClubFilter {
	static Map<String,String> map = new HashMap<String,String>();
	
	ArrayList<Club> getFilteredClubList();
	void setClubList(ArrayList<Club> newClubList);
	void addClub(Club newClub);
}
