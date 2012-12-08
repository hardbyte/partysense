package party.sense.app;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;
import android.widget.ToggleButton;

public class FragmentMenuScreen extends Fragment {
	View view;
	Button btnSongs, btnClubs, btnSettings;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		Bundle b = this.getArguments();
		int menuCnt = b.getInt("menuCnt");
		//int menuCnt = savedInstanceState.getInt("menuCnt");
		view = inflater.inflate(R.layout.layout_menu_screen, container,false);
		/*btnSongs = (Button) view.findViewById(R.id.btnSongs);
		btnSettings = (Button) view.findViewById(R.id.btnSettings);
		btnClubs = (Button) view.findViewById(R.id.btnClubs);
		
		btnSongs.setOnClickListener(new OnClickListener() {
			
			public void onClick(View v) {
				startActivity(new Intent("android.intent.action.PartySenseMainActivity"));
				getActivity().finish();
			}
		});
		
		btnClubs.setOnClickListener(new OnClickListener() {
			
			public void onClick(View v) {
				startActivity(new Intent("android.intent.action.PartySenseClubActivity"));
				getActivity().finish();
			}
		});*/
		
		/*switch(menuCnt)
		{
		case 0:
			btnSongs.setEnabled(false);
			break;
		case 1:
			btnClubs.setEnabled(false);
			break;
		case 2:
			btnSettings.setEnabled(false);
			break;
		}*/
		
		
		return view;		
	}
}
