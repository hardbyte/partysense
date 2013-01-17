//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import <UIKit/UIKit.h>
#import "ATPagingView.h"
#import "PSPageView.h"

@class MainMenuPageView;

@interface HomeViewController : ATPagingViewController {
    MainMenuPageView* mainMenuPageView;
    PSPageView* currentPageView;
}

@end
