//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>

@protocol MenuItemListDelegate <NSObject>
@required
-(void) onItemSelected:(int)index;
@end

@interface PSMenuItem : NSObject
{
	NSString* title;
    NSString* detail;
}
@property (nonatomic,retain) NSString* title;
@property (nonatomic,retain) NSString* detail;
@end;

@interface MenuItemListView : UITableView<UITableViewDelegate, UITableViewDataSource>
{
    NSMutableArray* items;
    id<MenuItemListDelegate> listDelegate;
}

@property (retain,setter=setItems:,getter=items)NSArray* items;
@property (nonatomic,retain) id<MenuItemListDelegate> listDelegate;

-(void)setItems:(NSArray*)itemsIn;
-(NSArray*)items;

@end
