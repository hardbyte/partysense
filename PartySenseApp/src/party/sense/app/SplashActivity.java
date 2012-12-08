package party.sense.app;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.widget.Toast;

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
	}

}