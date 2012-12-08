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
	private String mName;
	private String mAddress;
	private String mPhoneNumber;
	private String mEmail;
	private String mWebsite;
	private String mFwitterName;
	private String mFacebook;
	private String mGPlus;
	private String mOpenDuring;
	private long mLatitude;
	private long mLongitude;
	private List<String> mPhotoUrls;
	private List<PartySenseTag> mTags;
	private String mDescription;
	private String mUnstructuredInformation;
	
}
