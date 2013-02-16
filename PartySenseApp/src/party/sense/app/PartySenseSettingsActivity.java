package party.sense.app;

//import android.app.ActionBar;
//import android.app.FragmentTransaction;
import java.util.ArrayList;

import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class PartySenseSettingsActivity extends FragmentActivity {

    /**
     * The {@link android.support.v4.view.PagerAdapter} that will provide fragments for each of the
     * sections. We use a {@link android.support.v4.app.FragmentPagerAdapter} derivative, which will
     * keep every loaded fragment in memory. If this becomes too memory intensive, it may be best
     * to switch to a {@link android.support.v4.app.FragmentStatePagerAdapter}.
     */
    SectionsPagerAdapter mSectionsPagerAdapter;

    /**
     * The {@link ViewPager} that will host the section contents.
     */
    public static ViewPager mViewPager;
    public String[] segmentTitles = {"Menu","Settings","Map View"}; 
    ArrayList<Club> clubsList = new ArrayList<Club>();
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_party_sense_main);
        
        Bundle b = getIntent().getExtras();
        this.clubsList = b.getParcelableArrayList("party.sense.app.clubsList");
        Log.e("PartySenseMainActivity", "Club Name: " + clubsList.get(0).getName());
        
        mSectionsPagerAdapter = new SectionsPagerAdapter(getSupportFragmentManager(),clubsList);
        

        // Set up the ViewPager with the sections adapter.
        mViewPager = (ViewPager) findViewById(R.id.pager);
        mViewPager.setAdapter(mSectionsPagerAdapter);
        mViewPager.setCurrentItem(1);
        mViewPager.setBackgroundColor(Color.argb(128, 0, 0, 0));
        
        
    }
    
    /*
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_party_sense_main, menu);
        return true;
    }
     */
    public void onBackPressed(){
    	if(mViewPager.getCurrentItem()>0){
    		mViewPager.setCurrentItem(0);
    	}
    	else{
    		super.onBackPressed();
    	}
    }


    /**
     * A {@link FragmentPagerAdapter} that returns a fragment corresponding to one of the primary
     * sections of the app.
     */
    public class SectionsPagerAdapter extends FragmentPagerAdapter {

    	ArrayList<Club> clubsList = new ArrayList<Club>();
    	
        public SectionsPagerAdapter(FragmentManager fm, ArrayList<Club> clubsList) {
            super(fm);
            this.clubsList = clubsList;
            
        }
        
        @Override
        public Fragment getItem(int i) {
            Fragment fragment; //DummySectionFragment();
            Bundle b = new Bundle();
            b.putParcelableArrayList("party.sense.app.clubsList", this.clubsList);
            if(i ==0){
            	b.putInt("menuCnt", 4);
            	fragment = new FragmentMenuScreen();
            }
            else if(i ==1){
            	fragment = new FragmentSettingsScreen();
            }
            else{
            	fragment = new FragmentSearchScreen();
            }
        	fragment.setArguments(b);
            return fragment;
        }

        /**
         * Method to get count 
         */
        @Override
        public int getCount() {
            return 2;
        }

        @Override
        public CharSequence getPageTitle(int position) {
        	
        	return segmentTitles[position];
        	
            /*switch (position) {
                case 0: return getString(R.string.title_section1).toUpperCase();
                case 1: return getString(R.string.title_section2).toUpperCase();
                case 2: return getString(R.string.title_section3).toUpperCase();
            }
            return null;*/
        }
    }

    /**
     * A dummy fragment representing a section of the app, but that simply displays dummy text.
     */
    public static class DummySectionFragment extends Fragment {
        public DummySectionFragment() {
        }

        public static final String ARG_SECTION_NUMBER = "section_number";

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
            TextView textView = new TextView(getActivity());
            textView.setGravity(Gravity.CENTER);
            Bundle args = getArguments();
            textView.setText(Integer.toString(args.getInt(ARG_SECTION_NUMBER)));
            return textView;
        }
    }
}
