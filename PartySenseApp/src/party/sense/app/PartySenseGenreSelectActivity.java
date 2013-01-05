package party.sense.app;

import java.util.ArrayList;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.SparseBooleanArray;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

public class PartySenseGenreSelectActivity extends Activity {

	Button btnSavePrefs;
	ListView lView;
	SharedPreferences settings;
	SharedPreferences.Editor edit;
	ArrayList<String> genres = new ArrayList<String>();
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		
		genres.add("Rock");
		genres.add("HipHop");
		genres.add("Blues");
		genres.add("Jazz");
		genres.add("Techno");
		
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.layout_genre_screen);
	    btnSavePrefs = (Button) findViewById(R.id.btnSavePref);
	    lView = (ListView) findViewById(R.id.listView1);
	    lView.setAdapter(new ArrayAdapter<String>(this,
	            android.R.layout.simple_list_item_multiple_choice, genres));
	    lView.setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);
	    
	    
	    settings = getSharedPreferences(FragmentMenuScreen.PREFS_NAME, 0);
	    edit = settings.edit();
	    
	    for(int i = 0; i<lView.getCount(); i++){
	    	lView.setItemChecked(i, settings.getBoolean(genres.get(i), false));
	    }
	    
	    
	    
	    btnSavePrefs.setOnClickListener(new OnClickListener() {
			public void onClick(View v) {
				SparseBooleanArray checked = lView.getCheckedItemPositions();
			    for (int i = 0; i < checked.size(); i++) {
			        edit.putBoolean(genres.get(i), checked.get(checked.keyAt(i)));
			    }
			    Toast.makeText(getApplicationContext(), "Saved Preferences", Toast.LENGTH_LONG).show();
			    edit.commit();
			    finish();
			}
		});   
	}
}
