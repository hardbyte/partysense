//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import "MainMenuPageView.h"

@implementation MainMenuPageView


- (id)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
        listView = [[MenuItemListView alloc] initWithFrame: frame];
        
        NSMutableArray* itemArray = [[NSMutableArray alloc] initWithCapacity: 5];
        
        PSMenuItem* item1 = [[PSMenuItem alloc] init];
        item1.title = @"Recommended Clubs";
        [itemArray addObject: item1];
        
        PSMenuItem* item2 = [[PSMenuItem alloc] init];
        item2.title = @"Nearby Clubs";
        [itemArray addObject: item2];
        
        listView.items = itemArray;
        
        [self addSubview: listView];
        
        [listView retain];
    }
    return self;
}

- (void)dealloc {
    [super dealloc];
    [listView release];
}


@end
