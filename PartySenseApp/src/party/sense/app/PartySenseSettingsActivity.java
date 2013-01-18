package party.sense.app;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;

public class PartySenseSettingsActivity extends Activity {
	/** Called when the activity is first created. */
	
	ListView lvSettings;
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.layout_settings_screen);
	    
	    lvSettings = (ListView) findViewById(R.id.listSettings);
	    
	    ArrayList<String> optionStrings = new ArrayList<String>();
	    ArrayList<String> descStrings = new ArrayList<String>();
	    
	    optionStrings.add("Link your Spotify account");
	    optionStrings.add("Link your Rdio account");
	    optionStrings.add("Link your last.fm account");
	    optionStrings.add("Select genres manually");
	    optionStrings.add("Sign in");
	    
	    descStrings.add("Let us do the work for you");
	    descStrings.add("Scan your music library");
	    descStrings.add("Your music preferences");
	    descStrings.add("Select you preferred genres by hand");
	    descStrings.add("See your friends' activiy");
	    
	    
	    List<Map<String, String>> data = new ArrayList<Map<String, String>>();
	    for (int i = 0; i < optionStrings.size(); i++) {
	        Map<String, String> datum = new HashMap<String, String>(2);
	        datum.put("option", optionStrings.get(i));
	        datum.put("desc", descStrings.get(i));
	        data.add(datum);
	    }
	    
	    SimpleAdapter adapter = new SimpleAdapter(this, data,
	                                              android.R.layout.simple_list_item_2,
	                                              new String[] {"option", "desc"},
	                                              new int[] {android.R.id.text1,
	                                                         android.R.id.text2});
	    
	    lvSettings.setAdapter(adapter);
	    
	    lvSettings.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			public void onItemClick(AdapterView<?> adapter, View view, int pos, long id) {
				if(pos == 0){
					Toast.makeText(getApplicationContext(), "Spotify", Toast.LENGTH_LONG).show();
				}
				else if(pos == 1){
					Toast.makeText(getApplicationContext(), "Rdio", Toast.LENGTH_LONG).show();
				}
				else if(pos == 2){
					Toast.makeText(getApplicationContext(), "last.fm", Toast.LENGTH_LONG).show();
				}
				else if(pos == 3){
					startActivity(new Intent("android.intent.action.PartySenseGenreSelectActivity"));
				}
				else if(pos == 4){
					//Toast.makeText(getApplicationContext(), "Account Login", Toast.LENGTH_LONG).show();
					startActivity(new Intent("android.intent.action.PartySenseLoginActivity"));
					finish();
				}
				else{}
			}
	    });
	}
}
