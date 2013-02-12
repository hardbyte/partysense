//
//  PSCentral.m
//  PartySenseiOS
//
//  Created by Ahmed Hilali on 12/02/13.
//
//

#import "PSCentral.h"

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

-(void)blah
{
    NSLog(@"BLAH");
}

@end
