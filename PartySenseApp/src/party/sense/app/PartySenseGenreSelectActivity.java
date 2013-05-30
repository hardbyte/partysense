package party.sense.app;

import java.util.ArrayList;
import java.util.Arrays;

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
	
	
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		
		/*for(int i = 0; i < genreArray.length; i++){
			genres.add(genreArray[i]);
		}*/
		
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.layout_genre_screen);
	    btnSavePrefs = (Button) findViewById(R.id.btnSavePref);
	    lView = (ListView) findViewById(R.id.listView1);
	    lView.setAdapter(new ArrayAdapter<String>(this,
	            android.R.layout.simple_list_item_multiple_choice, genres));
	    lView.setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);
	    
	    
	    settings = getSharedPreferences(SplashActivity.PREFS_NAME, 0);
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
