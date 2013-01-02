/**
 * 
 */
package party.sense.app;

import java.util.List;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Class to represent our Data model of a Club
 * @author Tanmay Bhola [tanmay9@gmail.com]
 *
 */
public class Club implements Parcelable{
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
	
	private String latitude;
	private String longitude;
	
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
	
	public int describeContents() {
		return 0;
	}
	public void writeToParcel(Parcel out, int flags) {
		out.writeString(name);
		out.writeString(address);
		out.writeString(email);
		out.writeString(website);
		out.writeString(twitter);
		out.writeString(facebook);
		out.writeString(google_plus);
		out.writeString(time_created);
		out.writeString(time_updated);
		out.writeString(latitude);
		out.writeString(longitude);

		out.writeList(photo_urls);
		out.writeList(tags);
		
		out.writeString(description);
		out.writeString(unstructured_data);
		out.writeString(phone_number);
		out.writeString(phone_number);
		out.writeString(phone_number);
		out.writeString(phone_number);
		out.writeString(phone_number);
		out.writeString(phone_number);
		out.writeString(phone_number);
		out.writeString(phone_number);
		
		
	}
	
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getAddress() {
		return address;
	}
	public void setAddress(String address) {
		this.address = address;
	}
	public String getPhone_number() {
		return phone_number;
	}
	public void setPhone_number(String phone_number) {
		this.phone_number = phone_number;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public String getWebsite() {
		return website;
	}
	public void setWebsite(String website) {
		this.website = website;
	}
	public String getTwitter() {
		return twitter;
	}
	public void setTwitter(String twitter) {
		this.twitter = twitter;
	}
	public String getFacebook() {
		return facebook;
	}
	public void setFacebook(String facebook) {
		this.facebook = facebook;
	}
	public String getGoogle_plus() {
		return google_plus;
	}
	public void setGoogle_plus(String google_plus) {
		this.google_plus = google_plus;
	}
	public String getTime_created() {
		return time_created;
	}
	public void setTime_created(String time_created) {
		this.time_created = time_created;
	}
	public String getTime_updated() {
		return time_updated;
	}
	public void setTime_updated(String time_updated) {
		this.time_updated = time_updated;
	}
	public String getLatitude() {
		return latitude;
	}
	public void setLatitude(String latitude) {
		this.latitude = latitude;
	}
	public String getLongitude() {
		return longitude;
	}
	public void setLongitude(String longitude) {
		this.longitude = longitude;
	}
	public List<String> getPhoto_urls() {
		return photo_urls;
	}
	public void setPhoto_urls(List<String> photo_urls) {
		this.photo_urls = photo_urls;
	}
	public List<String> getTags() {
		return tags;
	}
	public void setTags(List<String> tags) {
		this.tags = tags;
	}
	public String getDescription() {
		return description;
	}
	public void setDescription(String description) {
		this.description = description;
	}
	public String getUnstructured_data() {
		return unstructured_data;
	}
	public void setUnstructured_data(String unstructured_data) {
		this.unstructured_data = unstructured_data;
	}
	public String getHours_default() {
		return hours_default;
	}
	public void setHours_default(String hours_default) {
		this.hours_default = hours_default;
	}
	public String getHours_monday() {
		return hours_monday;
	}
	public void setHours_monday(String hours_monday) {
		this.hours_monday = hours_monday;
	}
	public String getHours_tuesday() {
		return hours_tuesday;
	}
	public void setHours_tuesday(String hours_tuesday) {
		this.hours_tuesday = hours_tuesday;
	}
	public String getHours_wednesday() {
		return hours_wednesday;
	}
	public void setHours_wednesday(String hours_wednesday) {
		this.hours_wednesday = hours_wednesday;
	}
	public String getHours_thursday() {
		return hours_thursday;
	}
	public void setHours_thursday(String hours_thursday) {
		this.hours_thursday = hours_thursday;
	}
	public String getHours_friday() {
		return hours_friday;
	}
	public void setHours_friday(String hours_friday) {
		this.hours_friday = hours_friday;
	}
	public String getHours_saturday() {
		return hours_saturday;
	}
	public void setHours_saturday(String hours_saturday) {
		this.hours_saturday = hours_saturday;
	}
	public String getHours_sunday() {
		return hours_sunday;
	}
	public void setHours_sunday(String hours_sunday) {
		this.hours_sunday = hours_sunday;
	}

}
