//
//  PSCentral.h
//  PartySenseiOS
//
//  Created by Ahmed Hilali on 12/02/13.
//
//

#import <Foundation/Foundation.h>
#import "PSClub.h"

@interface PSCentral : NSObject
+(PSCentral*) sharedInstance;
-(void) getClubsListJSON: (void (^)(NSArray* json))callback;
-(void) getClubsList: (void (^)(NSArray* clubs))callback;
@end
