package party.sense.app;

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
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		
		view = inflater.inflate(R.layout.layout_songs_screen, container,false);
		
		
		lvClubList = (ListView) view.findViewById(R.id.recommended_club_listview);
		
		ClubListItem[] clubListArray = new ClubListItem[] {
				new ClubListItem(R.drawable.item_bg, "Degree","ELECTRO/HOUSE"),
				new ClubListItem(R.drawable.item_bg, "1885 Britomart","JAZZ/BLUES/FUNK"),
				new ClubListItem(R.drawable.item_bg, "A'isha","UNDERGROUND"),
				new ClubListItem(R.drawable.item_bg, "Club DELUXE","HOUSE/POP/RNB")
		};
		
		ClubListItemAdapter adapter = new ClubListItemAdapter(getActivity(), R.layout.club_item, clubListArray);
		
		lvClubList.setAdapter(adapter);
		
		//edtView.setInputType(0);
		
		return view;
	}
}
