//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import "RecommendedClubsPageView.h"



@implementation RecommendedClubsPageView

- (id)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
        listView = [[MenuItemListView alloc] initWithFrame: frame];
        
        [[PSCentral sharedInstance] getClubsList: ^(NSArray* clubs){
            [self performSelectorOnMainThread: @selector(setClubsData:) withObject:clubs waitUntilDone:NO];
        }];
        
        listView.listDelegate = self;
        [self addSubview: listView];
        [listView retain];
        
        [self setBackgroundColor: [UIColor blackColor]];
    }
    return self;
}

-(void)setClubsData: (id *) data
{
    NSArray* clubs = (NSArray*)data;
    NSInteger clubCount = [clubs count];

    NSMutableArray* itemArray = [[NSMutableArray alloc] initWithCapacity: clubCount];
    for(int i = 0;i < clubCount;i++)
    {
        PSMenuItem* menuItem = [[PSMenuItem alloc] init];
        PSClub* currentClub = [clubs objectAtIndex: i];
        
        menuItem.title = currentClub.name;
        [itemArray addObject: menuItem];
    }
    
    [listView setItems: itemArray];
    [itemArray release];
}

- (void)dealloc {
    [super dealloc];
    [listView release];
}

- (void) onItemSelected:(int)index
{
    //[pagingView setCurrentPageIndex: 1];
}

@end
