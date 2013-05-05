//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import "PartySenseAppDelegate.h"
#import "HomeViewController.h"


@implementation PartySenseAppDelegate

@synthesize window;
@synthesize navigationController;


#pragma mark -
#pragma mark Application lifecycle

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{    
    /*
    NSArray* paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSURL* localDataPath = [paths objectAtIndex: 0];
    NSData* localData = [NSData dataWithContentsOfFile: [NSString stringWithContentsOfURL:[localDataPath URLByAppendingPathComponent: @"local.json"] encoding:NSASCIIStringEncoding error:nil ]];
    
    if(localData)
    */
    {
        [self.window addSubview: self.navigationController.view];
    }
    /*
    else
    {
        // Do facebook login.
    }
     */
    
    [self.window makeKeyAndVisible];
    return YES;
}


- (void)applicationWillResignActive:(UIApplication *)application {
}


- (void)applicationDidEnterBackground:(UIApplication *)application {
}


- (void)applicationWillEnterForeground:(UIApplication *)application {
}


- (void)applicationDidBecomeActive:(UIApplication *)application {
}


- (void)applicationWillTerminate:(UIApplication *)application {
}


#pragma mark -
#pragma mark Memory management

- (void)applicationDidReceiveMemoryWarning:(UIApplication *)application {
}


- (void)dealloc {
    [window release];
    [super dealloc];
}


@end
