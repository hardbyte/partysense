package party.sense.app;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

public class SplashActivity extends Activity {

	
	
	
	/** Called when the activity is first created. */
	@Override
	
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
        setContentView(R.layout.splash);
        
	    Thread splashTimerThread = new Thread(){
	    	public void run(){
	    		try{
	    			int counter = 0;
	    			while(counter < 5000)
	    			{
	    				sleep(100);
	    				counter += 100;
	    			}
	    			startActivity(new Intent("android.intent.action.PartySenseMainActivity"));
	    		}
	    		catch(InterruptedException e){
	    			
	    		}
	    		finally{
	    			finish();
	    		}
	    	}
	    };
	    splashTimerThread.start();
	    
	    /*
	    // Adding functionality to Read/ Write to internal storage
	    String myString = "Testing writing to Club DB";
	    File partySenseDir = this.getDir("PartySenseData", Context.MODE_PRIVATE); //Creating an internal dir;
	    File clubDbFile = new File(partySenseDir, "clubDbTest.json"); //Getting a file within the dir.
	    FileOutputStream out = null;
	    try {
			out = new FileOutputStream(clubDbFile);
			out.write(myString.getBytes());
			out.close();
		} catch (FileNotFoundException fnfe) {
			fnfe.printStackTrace();
		} catch (IOException ioe) {
			ioe.printStackTrace();
		}
		
		FileInputStream in = null;
		try {
			in = openFileInput("filename.txt");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	    InputStreamReader inputStreamReader = new InputStreamReader(in);
	    BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
	    StringBuilder sb = new StringBuilder();
	    String line;
	    try {
			while ((line = bufferedReader.readLine()) != null) {
			    sb.append(line);
			}
			Log.e("SplashActivity", "Read : " + line);
		} catch (IOException e) {
			e.printStackTrace();
		}*/
	}
	
}
