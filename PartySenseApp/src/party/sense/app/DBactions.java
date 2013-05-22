package party.sense.app;

import java.security.KeyRep;
import java.util.ArrayList;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.os.Parcel;
import android.util.Log;

public class DBactions {
	private static final String DB_NAME = "partysenseDB";
	public static final String DB_TABLE = "userTable";
	public static final int DB_VERSION = 3;
	
	private DbHelper myHelper;
	private final Context myContext;
	private SQLiteDatabase myDB;
	
	public static final String keyID = "id";
	public static final String keyNAME = "name";
	public static final String keyADDRESS = "address";
	public static final String keyBANNER_IMAGE = "banner_image";
	public static final String keyCITY = "city";
	public static final String keyDESCRIPTION = "desc";
	public static final String keyIMAGES = "images";
	public static final String keyLATITUDE = "lat";
	public static final String keyLONGITUDE = "lot";
	public static final String keyPHONE = "phone";
	public static final String keyTAGS = "tags";
	public static final String keyWEBSITE = "website";
		
	private static class DbHelper extends SQLiteOpenHelper{

		public DbHelper(Context context) {
			super(context, DB_NAME, null, DB_VERSION);
			// TODO Auto-generated constructor stub
		}

		@Override
		public void onCreate(SQLiteDatabase db) {
			db.execSQL("CREATE TABLE " + DB_TABLE + " ("+
						keyID + " INTEGER PRIMARY KEY AUTOINCREMENT, " + 
						keyNAME + " TEXT, " +
						keyADDRESS+ " TEXT, " +
						keyBANNER_IMAGE + " TEXT, " +
						keyCITY + " TEXT, " +
						keyDESCRIPTION + " TEXT, " +
						keyIMAGES + " TEXT, " +
						keyLATITUDE + " REAL, " +
						keyLONGITUDE + " REAL, " +
						keyPHONE + " TEXT, " +
						keyTAGS + " TEXT, " +
						keyWEBSITE + " TEXT" +
						")"
			);
			
		}

		@Override
		public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
			// TODO Auto-generated method stub
			db.execSQL("DROP TABLE IF EXISTS " +  DB_TABLE);
			onCreate(db);
			
		}
	
	}

	public DBactions(Context c){
		myContext = c;
	}
	
	public DBactions open(){
		myHelper = new DbHelper(myContext);
		myDB = myHelper.getWritableDatabase();
		return this;
	}
	
	public void close(){
		myHelper.close();
	}

	public ArrayList<Club> getData(String sql){
		ArrayList<Club> clubList = new ArrayList<Club>();
		Cursor c = myDB.rawQuery("SELECT * from " + DB_TABLE, null);
		
		int iRow = c.getColumnIndex(keyID);
		int iClub = c.getColumnIndex(keyNAME);
		int iAddress = c.getColumnIndex(keyADDRESS);
		int iBanner = c.getColumnIndex(keyBANNER_IMAGE);
		int iCity = c.getColumnIndex(keyCITY);
		int iDesc = c.getColumnIndex(keyDESCRIPTION);
		int iImages = c.getColumnIndex(keyIMAGES);
		int iLat = c.getColumnIndex(keyLATITUDE);
		int iLon = c.getColumnIndex(keyLONGITUDE);
		int iPhone = c.getColumnIndex(keyPHONE);
		int iTags = c.getColumnIndex(keyTAGS);
		int iWebsite = c.getColumnIndex(keyWEBSITE);
		int i = 0;
		ArrayList<String> tags = new ArrayList<String>();
		
		for(c.moveToFirst(); !c.isAfterLast();c.moveToNext()){
			tags = new ArrayList<String>();
			Club newClub = new Club();
			newClub.setAddress(c.getString(iAddress));
			newClub.setDescription(c.getString(iDesc));
			newClub.setName(c.getString(iClub));
			newClub.setLatitude(Double.toString(c.getDouble(iLat)));
			newClub.setLongitude(Double.toString(c.getDouble(iLon)));
			String tagStr = "";
			tagStr = c.getString(iTags);
			String sArr[] = tagStr.split("#");
			
			for(int a = 0; a < sArr.length; a++){
				tags.add(sArr[a]);
				tagStr += sArr[a] + " ";
			}
			Log.i(newClub.getName(),tagStr);
			newClub.setTags(tags);
			newClub.setWebsite(c.getString(iWebsite));
			
			clubList.add(newClub);
			i++;
		}
		return clubList;
	}
	
	//public void write(String id, String name, String addr, String city, String desc, double lat, double lon, String phone, String tags, String website) {
	public void write(Club c) {
		ContentValues cv = new ContentValues();
		
		
		cv.put(keyNAME,c.getName());
		cv.put(keyADDRESS,c.getAddress());
		cv.put(keyBANNER_IMAGE, " ");
		cv.put(keyCITY,c.getCity());
		cv.put(keyDESCRIPTION,c.getDescription());
		cv.put(keyIMAGES,"");
		cv.put(keyLATITUDE,c.getLocation().getLatitude());
		cv.put(keyLONGITUDE,c.getLocation().getLongitude());
		cv.put(keyPHONE,c.getPhone_number());
		String tags = "";
		for(String s: c.getTags()){
			tags += "#" + s;
		}
		if(tags.length()<3) tags = "#";
		cv.put(keyTAGS,tags);
		cv.put(keyWEBSITE,c.getWebsite());
		
		//myDB.insert(DB_TABLE, null, cv);
		//myDB.rawQuery("insert or replace into "+ DB_TABLE + "("+ keyCLUB+", "+keyGENRE+" ) values ("+name+"," + genre + ")", null);
		if (myDB.rawQuery("SELECT * from " + DB_TABLE + " where " + keyNAME + " = \"" + c.getName() + "\"", null).getCount()>0){
			myDB.update(DB_TABLE, cv, keyNAME + " = \"" + c.getName() + "\"", null);
		}
		else{
			myDB.insert(DB_TABLE, null, cv);
		}

	}
	
	

}
