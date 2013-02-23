//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import <UIKit/UIKit.h>
#import "PSPageView.h"
#import "MenuItemListView.h"
#import "ATPagingView.h"
#import "PSCentral.h"


@interface NearbyClubsPageView : PSPageView<MenuItemListDelegate> {
    MenuItemListView* listView;
    UISlider* distanceSlider;
}

-(void)setClubsData: (id *) data;

@end
