//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import <UIKit/UIKit.h>
#import "PSPageView.h"
#import "MenuItemListView.h"
#import "ATPagingView.h"
#import "PSCentral.h"


@interface RecommendedClubsPageView : PSPageView<MenuItemListDelegate> {
    MenuItemListView* listView;

}

-(void)setClubsData: (id *) data;

@end
