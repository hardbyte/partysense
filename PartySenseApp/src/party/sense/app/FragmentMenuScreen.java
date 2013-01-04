package party.sense.app;

import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;
import android.widget.ToggleButton;

public class FragmentMenuScreen extends Fragment {
	public static final String PREFS_NAME = "PartySenseSharedPreff";
	View view;
	ListView lvMenu;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		Bundle b = this.getArguments();
		final int menuCnt = b.getInt("menuCnt");
		//int menuCnt = savedInstanceState.getInt("menuCnt");
		view = inflater.inflate(R.layout.layout_menu_screen, container,false);
		lvMenu = (ListView) view.findViewById(R.id.listMenu);
		
		lvMenu.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			public void onItemClick(AdapterView<?> adapter, View view, int pos, long id) {
				if(pos == menuCnt){
					
				}
				else{
	                if (pos == 0){
	                	startActivity(new Intent("android.intent.action.PartySenseMainActivity"));
	    				getActivity().finish();
	                }
	                else if (pos == 1){
	                	startActivity(new Intent("android.intent.action.PartySenseClubActivity"));
	    				getActivity().finish();
	                }
	                else if (pos == 2){
	                	startActivity(new Intent("android.intent.action.PartySenseMapActivity"));
	                }
	                else if (pos == 4){
	                	startActivity(new Intent("android.intent.action.PartySenseSettingsActivity"));
	                }
	                else{}
				}
            }
		});
		
		/*lvMenu.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
			public void onItemClick(AdapterView<?> arg0, View view, int position, long id) {
				Toast.ma
            }
			public void onItemSelected(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
				// TODO Auto-generated method stub
				
			}
			public void onNothingSelected(AdapterView<?> arg0) {
				// TODO Auto-generated method stub
				
			}
		});*/
		
		
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

class MenuAdapter extends ArrayAdapter<CharSequence> {

    public MenuAdapter(
            Context context, int textViewResId, CharSequence[] strings) {
        super(context, textViewResId, strings);
    }

    public static MenuAdapter createFromResource(
            Context context, int textArrayResId, int textViewResId) {

        Resources      resources = context.getResources();
        CharSequence[] strings   = resources.getTextArray(textArrayResId);

        return new MenuAdapter(context, textViewResId, strings);
    }

    public boolean areAllItemsEnabled() {
        return false;
    }

    public boolean isEnabled(int position) {
        // return false if position == position you want to disable
    	return false;
    }
}
