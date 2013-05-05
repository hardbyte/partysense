//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import "NearbyClubsPageView.h"

@implementation NearbyClubsPageView

- (id)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
        CGRect listRect = frame;
        listRect.size.height -= 40;
        
        listView = [[MenuItemListView alloc] initWithFrame: listRect];
        listView.listDelegate = self;
        [self addSubview: listView];
        [listView retain];
        
        distanceSlider = [[UISlider alloc] initWithFrame: CGRectMake(0, 440, 320, 40)];
        [distanceSlider setMinimumValue:0.01];
        [distanceSlider setMaximumValue:1];
        [distanceSlider setValue:0.5];
        [distanceSlider setUserInteractionEnabled:YES];
        [self addSubview: distanceSlider];
        
        [[PSCentral sharedInstance] getClubsList: ^(NSArray* clubs){
            [self performSelectorOnMainThread: @selector(setClubsData:) withObject:clubs waitUntilDone:NO];
        }];
        
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
        
        NSString* genreString = [[NSString alloc] init];
        for(int j = 0;j < [currentClub.tags count];j++)
        {
            genreString = [genreString stringByAppendingString: [currentClub.tags objectAtIndex: j]];
            if(j < [currentClub.tags count] - 1)
                genreString = [genreString stringByAppendingString: @"/"];
        }

        menuItem.detail = genreString;
        
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
