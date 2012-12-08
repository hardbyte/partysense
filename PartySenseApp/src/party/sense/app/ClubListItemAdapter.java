package party.sense.app;

//http://www.ezzylearning.com/tutorial.aspx?tid=1763429

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

public class ClubListItemAdapter extends ArrayAdapter<ClubListItem>{

    Context context; 
    int layoutResourceId;    
    ClubListItem data[] = null;
    
    public ClubListItemAdapter(Context context, int layoutResourceId, ClubListItem[] data) {
        super(context, layoutResourceId, data);
        this.layoutResourceId = layoutResourceId;
        this.context = context;
        this.data = data;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View row = convertView;
        ClubListItemHolder holder = null;
        
        if(row == null)
        {
            LayoutInflater inflater = ((Activity)context).getLayoutInflater();
            row = inflater.inflate(layoutResourceId, parent, false);
            
            holder = new ClubListItemHolder();
            holder.tvClubName = (TextView)row.findViewById(R.id.club_item_tvClubName);
            holder.tvClubSub = (TextView)row.findViewById(R.id.club_item_tvClubSub);
            holder.imgClubBG = (ImageView)row.findViewById(R.id.club_item_imgClubBG);
            
            row.setTag(holder);
        }
        else
        {
            holder = (ClubListItemHolder)row.getTag();
        }
        
        ClubListItem clubListItem = data[position];
        holder.tvClubName.setText(clubListItem.ClubName);
        holder.tvClubSub.setText(clubListItem.ClubSub);
        holder.imgClubBG.setImageResource(clubListItem.ClubBG);
        
        return row;
    }
    
    static class ClubListItemHolder
    {
        ImageView imgClubBG;
        TextView tvClubName;
        TextView tvClubSub;
    }
}
