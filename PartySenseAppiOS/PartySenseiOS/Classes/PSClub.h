//
//  PSClub.h
//  PartySenseiOS
//
//  Created by Ahmed Hilali on 16/02/13.
//
//

#import <Foundation/Foundation.h>

@interface PSClub : NSObject

@property (retain, nonatomic) NSString* name;
@property (retain, nonatomic) NSString* address;
@property (retain, nonatomic) NSString* phone_number;
@property (retain, nonatomic) NSString* email;
@property (retain, nonatomic) NSString* website;
@property (retain, nonatomic) NSString* twitter;
@property (retain, nonatomic) NSString* facebook;
@property (retain, nonatomic) NSString* google_plus;
@property (retain, nonatomic) NSString* time_created;
@property (retain, nonatomic) NSString* time_updated;
@property (retain, nonatomic) NSString* latitude;
@property (retain, nonatomic) NSString* longitude;

@property (retain, nonatomic) NSMutableArray* photo_urls;
@property (retain, nonatomic) NSMutableArray* tags;
@property (retain, nonatomic) NSString* description;
@property (retain, nonatomic) NSString* unstructured_data;

@property (retain, nonatomic) NSString* hours_default;
@property (retain, nonatomic) NSString* hours_monday;
@property (retain, nonatomic) NSString* hours_tuesday;
@property (retain, nonatomic) NSString* hours_wednesday;
@property (retain, nonatomic) NSString* hours_thursday;
@property (retain, nonatomic) NSString* hours_friday;
@property (retain, nonatomic) NSString* hours_saturday;
@property (retain, nonatomic) NSString* hours_sunday;

@end
