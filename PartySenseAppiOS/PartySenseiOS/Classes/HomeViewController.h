//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import <UIKit/UIKit.h>
#import "ATPagingView.h"
#import "PSPageView.h"
#import "MainMenuPageView.h"

@class RecommendedClubsPageView;

@interface HomeViewController : ATPagingViewController<PSMainMenuPageDelegate> {
    MainMenuPageView* mainMenuPageView;
    RecommendedClubsPageView* recommendedPageView;
    PSPageView* currentPageView;
    NSInteger selectedIndex;
}

@end
