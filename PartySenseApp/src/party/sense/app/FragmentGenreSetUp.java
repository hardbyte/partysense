package party.sense.app;

import java.util.ArrayList;
import java.util.Map;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.util.SparseBooleanArray;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

public class FragmentGenreSetUp extends Fragment {

	ListView lView;
	SharedPreferences settings;
	SharedPreferences.Editor edit;
	static ArrayList<String> genres = new ArrayList<String>();
	
	
	static{
		genres.add("Blues");
		genres.add("Country");
		genres.add("Electronic");
		genres.add("Disco");
		genres.add("House");
		genres.add("Hiphop");
		genres.add("Jazz");
		genres.add("Latin");
		genres.add("Pop");
		genres.add("Reggae");
		genres.add("RnB");
		genres.add("Rock");
	}
	View view;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		view = inflater.inflate(R.layout.frag_genre, container,false);
		lView = (ListView) view.findViewById(R.id.lvGenreFrag);
		lView.setAdapter(new ArrayAdapter<String>(getActivity(),
	            android.R.layout.simple_list_item_multiple_choice, genres));
	    lView.setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);
	    settings = getActivity().getSharedPreferences(SplashActivity.PREFS_NAME, 0);
	    edit = settings.edit();
	    refreshList();
	    /*Map<String, ?> m = settings.getAll();
	    for(Map.Entry<String,?> ms : m.entrySet()){
	    	Log.d("PREF",ms.getKey());
	    }*/
		return view;
	}
	
	private void refreshList(){
		for(int i = 0; i<lView.getCount(); i++){
	    	lView.setItemChecked(i, settings.getBoolean(genres.get(i), false));
	    	
	    }
	}
	
	public boolean writeGenre(){
		int genreSelectCount = 0;
		SparseBooleanArray checked = lView.getCheckedItemPositions();
	    for (int i = 0; i < checked.size(); i++) {
	        edit.putBoolean(genres.get(i), checked.get(checked.keyAt(i)));
	        if(checked.get(checked.keyAt(i))){
	        	genreSelectCount++;
	        }
	    }
	    if(genreSelectCount < 1){
	    	return false;
	    }
	    else{
	    	edit.commit();
	    	refreshList();
			return true;
	    }
	    
	}
	
	public ArrayList<Boolean>genresSelected(){
		SparseBooleanArray checked = lView.getCheckedItemPositions();
		ArrayList<Boolean> selectionValues = new ArrayList<Boolean>();
		selectionValues.clear();
	    for (int i = 0; i < checked.size(); i++) {
	    	selectionValues.add(checked.get(checked.keyAt(i)));
	    }
	    return selectionValues;
	    
	}
	
	@Override
	public void onResume() {
		// TODO Auto-generated method stub
		super.onResume();
		refreshList();
	}
	
	
	
}
