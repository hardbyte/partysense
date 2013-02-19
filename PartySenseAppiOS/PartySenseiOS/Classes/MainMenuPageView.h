//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import <UIKit/UIKit.h>
#import "PSPageView.h"
#import "MenuItemListView.h"
#import "ATPagingView.h"

@protocol PSMainMenuPageDelegate <NSObject>
-(void) onPageSelected: (NSInteger)index;
@end

enum E_MENU_PAGE
{
    EMP_RECOMMENDED_CLUBS,
    EMP_NEARBY_CLUBS,
    EMP_MAP_VIEW,
    EMP_FRIENDS,
    EMP_SETTINGS,
    
    EMP_COUNT
};

static NSString* pageStrings[EMP_COUNT] =
{
    @"Recommended Clubs",
    @"Nearby Clubs",
    @"Map View",
    @"Friends",
    @"Settings"
};

@interface MainMenuPageView : PSPageView<MenuItemListDelegate> {
    MenuItemListView* listView;
    id<PSMainMenuPageDelegate> delegate;
}

@property (nonatomic, retain) id<PSMainMenuPageDelegate> delegate;

@end
