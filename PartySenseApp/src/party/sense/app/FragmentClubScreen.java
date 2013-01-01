package party.sense.app;
import java.util.ArrayList;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.Toast;

public class FragmentClubScreen extends Fragment {

	ListView lvClubList;
	Button btnTest;
	ClubListItemAdapter adapter;
	View view;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		
		view = inflater.inflate(R.layout.layout_club_screen, container,false);
		//edtView.setInputType(0);
		lvClubList = (ListView) view.findViewById(R.id.nearby_club_listview);
		btnTest = (Button) view.findViewById(R.id.btnTest);
		
		btnTest.setOnClickListener(new OnClickListener() {
			
			public void onClick(View v) {
				addClubItem(R.drawable.item_bg, "ClubTANMAY","10m");
			}
		});
		
		ArrayList<ClubListItem> clubListArray = new ArrayList<ClubListItem>();
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "Degree","10m"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "1885 Britomart","102m"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "A'isha","2km"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "Club DELUXE","3.5km"));
		
		adapter = new ClubListItemAdapter(getActivity(), R.layout.club_item, clubListArray);
		
		lvClubList.setAdapter(adapter);
		
		
		
		return view;
	}
	
	private void addClubItem(int imgID, String clubName, String clubSub){
		adapter.add(new ClubListItem(imgID, clubName, clubSub));
	}
}
