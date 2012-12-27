package party.sense.app;

import java.util.ArrayList;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.Toast;

public class FragmentSongsScreen extends Fragment {

	View view;
	ListView lvClubList;
	ClubListItemAdapter adapter;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		
		view = inflater.inflate(R.layout.layout_songs_screen, container,false);
		
		
		lvClubList = (ListView) view.findViewById(R.id.recommended_club_listview);
		
		ArrayList<ClubListItem> clubListArray = new ArrayList<ClubListItem>();
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "Degree","ELECTRO/HOUSE"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "1885 Britomart","JAZZ/BLUES/FUNK"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "A'isha","UNDERGROUND"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "Club DELUXE","HOUSE/POP/RNB"));
		
		ClubListItemAdapter adapter = new ClubListItemAdapter(getActivity(), R.layout.club_item, clubListArray);
		
		lvClubList.setAdapter(adapter);
		
		//edtView.setInputType(0);
		
		return view;
	}
	
	private void addClubItem(int imgID, String clubName, String clubSub){
		adapter.add(new ClubListItem(imgID, clubName, clubSub));
	}
}
