//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import <UIKit/UIKit.h>
#import "ATPagingView.h"

@interface PSPageView : UIView {
    ATPagingView* pagingView;
    NSString* title;
}

@property (nonatomic,retain) NSString* title;
@property (nonatomic,retain) ATPagingView* pagingView;

@end
