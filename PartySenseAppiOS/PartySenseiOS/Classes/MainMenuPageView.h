//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import <UIKit/UIKit.h>
#import "PSPageView.h"
#import "MenuItemListView.h"
#import "ATPagingView.h"

enum E_MENU_PAGE
{
    EMP_RECOMMENDED_CLUBS,
    EMP_NEARBY_CLUBS,
    EMP_MAP_VIEW,
    EMP_FRIENDS,
    EMP_SETTINGS,
    
    EMP_COUNT
};

@interface MainMenuPageView : PSPageView<MenuItemListDelegate> {
    MenuItemListView* listView;

}

@end
