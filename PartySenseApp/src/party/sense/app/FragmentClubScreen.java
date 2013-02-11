package party.sense.app;
import java.util.ArrayList;

import android.R.integer;
import android.content.Intent;
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
				PartySenseClubActivity.mViewPager.setCurrentItem(0);
			}
		});
		
		ArrayList<ClubListItem> clubListArray = new ArrayList<ClubListItem>();
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "Degree","10m"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "1885 Britomart","102m"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "A'isha","2km"));
		clubListArray.add(new ClubListItem(R.drawable.item_bg, "Club DELUXE","3.5km"));
		
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
		
		return view;
	}
	
	private void addClubItem(int imgID, String clubName, String clubSub){
		adapter.add(new ClubListItem(imgID, clubName, clubSub));
	}
	
	
	
}
