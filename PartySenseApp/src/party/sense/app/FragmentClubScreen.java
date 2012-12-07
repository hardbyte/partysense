package party.sense.app;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

public class FragmentClubScreen extends Fragment {

	View view;
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
	{
		
		view = inflater.inflate(R.layout.layout_club_screen, container,false);
		EditText edtView=(EditText) view.findViewById(R.id.editText1);
		ImageButton myBtn = (ImageButton) view.findViewById(R.id.imageButton1);
		myBtn.setFocusableInTouchMode(true);
		myBtn.requestFocus();
		//edtView.setInputType(0);
		
		myBtn.setOnClickListener(new OnClickListener() {
			
			public void onClick(View v) {
				Toast.makeText(getActivity(), "DEVA IS AWESOME!!", Toast.LENGTH_SHORT).show();
				
			}
		});
		
		return view;
	}
}
