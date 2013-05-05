//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import "PSPageView.h"


@implementation PSPageView
@synthesize pagingView;
@synthesize title;

- (id)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
    }
    return self;
}

- (void)dealloc {
    [super dealloc];
}

@end
