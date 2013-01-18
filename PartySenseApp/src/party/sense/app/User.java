package party.sense.app;
import java.util.List;


/**
 * 
 */

/**
 * Class to represent the Data Model of a User of PartySense
 * @author Tanmay Bhola
 *
 */
public class User {

	private String name;
	private String address;
	private String email;
	private List<String> clubs_favourite;
	private List<String> clubs_visited;
	private List<String> favourite_genres;
	private List<String> friends_registered;
	private List<String> friends_facebook;
	
	private double latitude;
	private double longitude;
	private String time_location_updated; 

	private String facebook_id;
	private String spotify_id;
	private String last_fm_id; 

	private String profile_picture_url;
}
