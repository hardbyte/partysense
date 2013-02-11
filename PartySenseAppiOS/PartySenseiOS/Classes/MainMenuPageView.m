//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import "MainMenuPageView.h"



@implementation MainMenuPageView

- (id)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
        listView = [[MenuItemListView alloc] initWithFrame: frame];
        
        NSMutableArray* itemArray = [[NSMutableArray alloc] initWithCapacity: EMP_COUNT];
        
        for(int i = 0;i < EMP_COUNT;i++)
        {
            PSMenuItem* menuItem = [[PSMenuItem alloc] init];
            menuItem.title = pageStrings[i];
            [itemArray addObject: menuItem];
        }
        
        listView.items = itemArray;
        listView.listDelegate = self;
        
        [self addSubview: listView];
        
        [listView retain];
        [itemArray release];
        
        [self setBackgroundColor: [UIColor blackColor]];
    }
    return self;
}

- (void)dealloc {
    [super dealloc];
    [listView release];
}

- (void) onItemSelected:(int)index
{
    switch (index) {
        case EMP_RECOMMENDED_CLUBS:
            
            break;
            
        default:
            break;
    }
    
    [pagingView setCurrentPageIndex: 1];
}

@end
