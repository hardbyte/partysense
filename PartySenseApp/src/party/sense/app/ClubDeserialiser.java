/**
 * 
 */
package party.sense.app;

import java.lang.reflect.Type;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;

/**
 * Class incorporating the deserialisation strategy for Clubs
 * @author Tanmay Bhola (tanmay9@gmail.com)
 * @deprecated This class is deprecated
 * @see http://stackoverflow.com/questions/7883615/custom-deserialization-in-gson
 * @see http://stackoverflow.com/questions/8533020/gson-custom-object-deserialization?rq=1
 * @see http://stackoverflow.com/questions/8165412/gson-custom-deserializing-logic-based-on-field-name
 * @see http://albertattard.blogspot.co.nz/2012/06/practical-example-of-gson-part-2.html
 * 
 */
public class ClubDeserialiser implements JsonDeserializer<Club> {
	
	
	public Club deserialize(JsonElement json, Type typeOfT,
			JsonDeserializationContext context) throws JsonParseException {

		Club club  = new Club();
		JsonObject clubJsonObject = json.getAsJsonObject();
		
		JsonElement element = clubJsonObject.get("name");
		if(element != null) { 
			club.setName(element.getAsString());
		}
		
		club.setAddress(clubJsonObject.get("address").getAsString());
		club.setPhone_number(clubJsonObject.get("phone_number").getAsString());
		club.setEmail(clubJsonObject.get("email").getAsString());
		club.setWebsite(clubJsonObject.get("website").getAsString());
		club.setTwitter(clubJsonObject.get("twitter").getAsString());
		club.setFacebook(clubJsonObject.get("facebook").getAsString());
		club.setGoogle_plus(clubJsonObject.get("google_plus").getAsString());
		club.setTime_created(clubJsonObject.get("time_created").getAsString());
		club.setTime_updated(clubJsonObject.get("time_updated").getAsString());
		club.setLatitude(clubJsonObject.get("latitude").getAsString());
		club.setLongitude(clubJsonObject.get("longitude").getAsString());
		
		//GsonBuilder gsonBuilder = new GsonBuilder();
		//gsonBuilder.registerTypeAdapter(Photos.class, new PhotosDeserialiser());
		//Gson gson = gsonBuilder.create();
		
		
		// TODO: Complete implementation if required
		
		return club;
	}
	
	

}
