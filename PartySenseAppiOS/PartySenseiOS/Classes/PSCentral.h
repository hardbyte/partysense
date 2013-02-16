//
//  PSCentral.h
//  PartySenseiOS
//
//  Created by Ahmed Hilali on 12/02/13.
//
//

#import <Foundation/Foundation.h>

@interface PSCentral : NSObject
+(PSCentral*) sharedInstance;
-(void) getClubsList: (void (^)(NSDictionary* json))callback;
@end
