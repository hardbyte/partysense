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

-(void) getClubsList: (void (^)(NSDictionary* json))callback
{
    NSURL* url = [NSURL URLWithString: @"http://partysenseapp.appspot.com/api/clubs-dump"];
    __block ASIHTTPRequest* request = [ASIHTTPRequest requestWithURL: url];
    [request setCompletionBlock: ^{
        // Parse the response data as JSON and provide it the callback block.
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData: [request responseData] options: nil error: nil];
        callback(json);
    }];
}

@end
