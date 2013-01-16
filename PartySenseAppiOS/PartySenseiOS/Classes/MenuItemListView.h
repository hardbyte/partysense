//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>

@interface PSMenuItem : NSObject
{
	NSString* title;
}
@property (nonatomic,retain) NSString* title;
@end;

@interface MenuItemListView : UITableView<UITableViewDelegate, UITableViewDataSource>
{
     NSMutableArray* items;
}

@property (retain,setter=setItems:,getter=items)NSArray* items;

-(void)setItems:(NSArray*)itemsIn;
-(NSArray*)items;

@end
