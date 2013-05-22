package party.sense.app;

import java.util.ArrayList;

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
	
	View view;
	ListView lvMenu;
	ArrayList<Club> clubsList = new ArrayList<Club>();
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		Bundle b = this.getArguments();
		final int menuCnt = b.getInt("menuCnt");
		//int menuCnt = savedInstanceState.getInt("menuCnt");
		view = inflater.inflate(R.layout.layout_menu_screen, container,false);
		lvMenu = (ListView) view.findViewById(R.id.listMenu);
		clubsList = b.getParcelableArrayList("party.sense.app.clubsList");
		
		lvMenu.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			public void onItemClick(AdapterView<?> adapter, View view, int pos, long id) {
				if(pos == menuCnt){
					if (pos == 0){
						PartySenseMainActivity.mViewPager.setCurrentItem(1);
	                }
	                else if (pos == 1){
	                	PartySenseClubActivity.mViewPager.setCurrentItem(1);
	                }
	                else if (pos == 4){
	                	PartySenseSettingsActivity.mViewPager.setCurrentItem(1);
	                }
				}
				else{
	                if (pos == 0){
	                	Bundle b = new Bundle();
	                	Intent i = new Intent("android.intent.action.PartySenseMainActivity");
	                    b.putParcelableArrayList("party.sense.app.clubsList", clubsList);
	        			i.putExtras(b);
	        			startActivity(i);
	    				getActivity().finish();
	                }
	                else if (pos == 1){
	    				Bundle b = new Bundle();
	                	Intent i = new Intent("android.intent.action.PartySenseClubActivity");
	                    b.putParcelableArrayList("party.sense.app.clubsList", clubsList);
	        			i.putExtras(b);
	        			startActivity(i);
	    				getActivity().finish();
	                }
	                else if (pos == 2){
	                	Bundle b = new Bundle();
	                	Intent i = new Intent("android.intent.action.PartySenseMapActivity");
	                    b.putParcelableArrayList("party.sense.app.clubsList", clubsList);
	        			i.putExtras(b);
	        			startActivity(i);
	                }
	                else if (pos == 4){
	                	Bundle b = new Bundle();
	                	Intent i = new Intent("android.intent.action.PartySenseSettingsActivity");
	                    b.putParcelableArrayList("party.sense.app.clubsList", clubsList);
	        			i.putExtras(b);
	        			startActivity(i);
	    				getActivity().finish();
	                }
	                else{}
				}
            }
		});
		
		
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
