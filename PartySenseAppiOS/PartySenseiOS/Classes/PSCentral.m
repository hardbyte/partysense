//
//  PSCentral.m
//  PartySenseiOS
//
//  Created by Ahmed Hilali on 12/02/13.
//
//

#import "PSCentral.h"
#import "ASIHTTPRequest.h"

@implementation PSCentral

static PSCentral *sharedSingleton;

+ (void)initialize
{
    static BOOL initialized = NO;
    if(!initialized)
    {
        initialized = YES;
        sharedSingleton = [[PSCentral alloc] init];
    }
}

+(PSCentral*) sharedInstance
{
    return sharedSingleton;
}

-(void) getClubsListJSON: (void (^)(NSArray* json))callback
{
    NSURL* url = [NSURL URLWithString: @"http://partysenseapp.appspot.com/api/clubs-dump"];
    __block ASIHTTPRequest* request = [ASIHTTPRequest requestWithURL: url];
    [request setCompletionBlock: ^{
        // Parse the response data as JSON and provide it the callback block.
        NSArray* json = [NSJSONSerialization JSONObjectWithData: [request responseData] options: nil error: nil];
        callback(json);
    }];
    
    [request startAsynchronous];
}

-(void) getClubsList: (void (^)(NSArray* clubs))callback
{
    [self getClubsListJSON:^(NSArray* json)
     {
         NSInteger clubCount = [json count];
         
         NSMutableArray* itemArray = [[NSMutableArray alloc] initWithCapacity: clubCount];
         for(int i = 0;i < clubCount;i++)
         {
             PSClub* club = [[PSClub alloc] init];
             NSDictionary* currentItem = [json objectAtIndex: i];
             
             club.name = [currentItem objectForKey: @"name"];
             club.address = [currentItem objectForKey: @"address"];
             club.phone_number = [currentItem objectForKey: @"phone_number"];
             club.email = [currentItem objectForKey: @"email"];
             club.website = [currentItem objectForKey: @"website"];
             club.twitter = [currentItem objectForKey: @"twitter"];
             club.facebook = [currentItem objectForKey: @"facebook"];
             club.google_plus = [currentItem objectForKey: @"google_plus"];
             club.time_created = [currentItem objectForKey: @"time_created"];
             club.time_updated = [currentItem objectForKey: @"time_updated"];
             club.latitude = [currentItem objectForKey: @"latitude"];
             club.longitude = [currentItem objectForKey: @"longitude"];

             club.description = [currentItem objectForKey: @"description"];
             club.unstructured_data = [currentItem objectForKey: @"unstructured_data"];
             
             club.hours_default = [currentItem objectForKey: @"hours_default"];
             club.hours_monday = [currentItem objectForKey: @"hours_monday"];
             club.hours_tuesday = [currentItem objectForKey: @"hours_tuesday"];
             club.hours_wednesday = [currentItem objectForKey: @"hours_wednesday"];
             club.hours_thursday = [currentItem objectForKey: @"hours_thursday"];
             club.hours_friday = [currentItem objectForKey: @"hours_friday"];
             club.hours_saturday = [currentItem objectForKey: @"hours_saturday"];
             club.hours_sunday = [currentItem objectForKey: @"hours_sunday"];
             [itemArray addObject: club];
         }
         
         callback(itemArray);
     }];
}

@end
