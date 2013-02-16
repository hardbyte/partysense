package party.sense.app;
import java.util.ArrayList;

//https://developers.google.com/maps/documentation/android/v1/hello-mapview

import android.app.AlertDialog;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.drawable.Drawable;

import com.google.android.maps.ItemizedOverlay;
import com.google.android.maps.MapView;
import com.google.android.maps.OverlayItem;


public class MyLocationItem extends ItemizedOverlay<OverlayItem>{

	private ArrayList<OverlayItem> mOverlays = new ArrayList<OverlayItem>();
	private Context mContext;
	@Override
	public void draw(Canvas canvas, MapView mapView, boolean shadow) {
        super.draw(canvas, mapView, false);
    }
	
	public MyLocationItem(Drawable defaultMarker,Context context) {
		super(boundCenterBottom(defaultMarker));

		  mContext = context;
			populate();
	}
	
	public void clear(){
		mOverlays.clear();
		populate();
	}
	
	public void addOverlay(OverlayItem overlay) {
	    mOverlays.add(overlay);
	    populate();
	}
	
	@Override
	protected OverlayItem createItem(int i) {
		// TODO Auto-generated method stub
		return mOverlays.get(i);
	}
	@Override
	public int size() {
		// TODO Auto-generated method stub
		return mOverlays.size();
	}
	
	@Override
	protected boolean onTap(int index) {
	  /*OverlayItem item = mOverlays.get(index);
	  AlertDialog.Builder dialog = new AlertDialog.Builder(mContext);
	  dialog.setTitle(item.getTitle());
	  dialog.setMessage(item.getSnippet());
	  dialog.show();*/
	  return true;
	}

}
