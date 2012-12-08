/**
 * 
 */
package party.sense.app;

import java.util.List;

/**
 * Class to represent our Data model of a Club
 * @author Tanmay Bhola [tanmay9@gmail.com]
 *
 */
public class Club {
	private String name;
	private String address;
	private String phone_number;
	private String email;
	private String website;
	private String twitter;
	private String facebook;
	private String google_plus;
	
	private String time_created;
	private String time_updated;
	
	private long latitude;
	private long longitude;
	
	private List<String> photo_urls;
	
	private List<String> tags;
	
	private String description;
	private String unstructured_data;
	
	private String hours_default;
	private String hours_monday;
	private String hours_tuesday; 
	private String hours_wednesday; 
	private String hours_thursday; 
	private String hours_friday; 
	private String hours_saturday;
	private String hours_sunday;
}
