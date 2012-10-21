package party.sense.app;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ImageButton;

public class dummyFrag extends Fragment {

	View view;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		
		view = inflater.inflate(R.layout.layout_club_screen, container,false);
		EditText edtView=(EditText) view.findViewById(R.id.editText1);
		ImageButton myBtn = (ImageButton) view.findViewById(R.id.imageButton1);
		myBtn.setFocusableInTouchMode(true);
		myBtn.requestFocus();
		edtView.setInputType(0);
		return view;
	}
}
