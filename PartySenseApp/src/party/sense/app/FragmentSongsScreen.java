package party.sense.app;

import java.util.ArrayList;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.Toast;

public class FragmentSongsScreen extends Fragment {

	View view;
	ListView lvClubList;
	ClubListItemAdapter adapter;
	ArrayList<Club> clubList;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		
		view = inflater.inflate(R.layout.layout_songs_screen, container,false);
		Bundle b = this.getArguments();
		clubList = b.getParcelableArrayList("party.sense.app.clubsList");
		
		lvClubList = (ListView) view.findViewById(R.id.recommended_club_listview);
		
		ArrayList<ClubListItem> clubListArray = new ArrayList<ClubListItem>();
		/*clubListArray.add(new ClubListItem(R.drawable.item_bg, clubList.get(0).getName(),"ELECTRO/HOUSE"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "1885 Britomart","JAZZ/BLUES/FUNK"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "A'isha","UNDERGROUND"));*/
		
		adapter = new ClubListItemAdapter(getActivity(), R.layout.club_item, clubListArray);
		
		lvClubList.setAdapter(adapter);
		
		for(Club c: clubList){
			addClubItem(c);
		}
		
		//edtView.setInputType(0);
		
		lvClubList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			public void onItemClick(AdapterView<?> adapterView, View view, int pos, long id) {
            	Intent detailIntent = new Intent("android.intent.action.PartySenseDetailsActivity");
            	detailIntent.putExtra(PartySenseDetailsActivity.BUNDLE_ID_CLUB_NAME, clubList.get(pos).getName());
            	detailIntent.putExtra(PartySenseDetailsActivity.BUNDLE_ID_CLUB_GENRE, getGenreString(clubList.get(pos).getTags()));
            	detailIntent.putExtra(PartySenseDetailsActivity.BUNDLE_ID_CLUB_ADDRESS, clubList.get(pos).getAddress());
            	detailIntent.putExtra(PartySenseDetailsActivity.BUNDLE_ID_CLUB_WEBSITE, clubList.get(pos).getWebsite());
            	detailIntent.putExtra(PartySenseDetailsActivity.BUNDLE_ID_CLUB_DESCRIPTION, clubList.get(pos).getDescription());
            	startActivity(detailIntent);
            }
		});
		
		return view;
	}
	
	private void addClubItem(int imgID, String clubName, String clubSub){
		adapter.add(new ClubListItem(imgID, clubName, clubSub));
	}
	
	private void addClubItem(Club c){
		
		adapter.add(new ClubListItem(R.drawable.item_bg, c.getName(),getGenreString(c.getTags())));	
	}
	
	private String getGenreString(ArrayList<String> tagsList) {
		String genreString ="";
		for(String tags : tagsList){
			if (tags.split("_")[0].toLowerCase().equals("music")){
				genreString += "/" + tags.split("_")[1].toUpperCase(); 
			}
		}
		if (genreString.length()>1){
			genreString = genreString.substring(1);
		}
		return genreString;
	}
}
