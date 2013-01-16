//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import "MenuItemListView.h"

@implementation PSMenuItem
@synthesize title;
@end

@implementation MenuItemListView

@synthesize items;

- (id)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
		items = [[NSMutableArray alloc] init];

        self.delegate = self;
        self.dataSource = self;
        self.backgroundColor = [UIColor clearColor];    
    }
    return self;
}

- (void)dealloc {
    [super dealloc];
    [items release];
}

- (void)setItems:(NSArray*)itemsIn
{
	@synchronized(items)
	{
		[items removeAllObjects];
		[items addObjectsFromArray:itemsIn];
	}
}

- (NSArray*)items {
    return items;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
	@synchronized(items) {
        //printf("Items count requested %d", [items count]);
		return [items count];
	}
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString* cellIdent = @"PartySenseIdent";
    UITableViewCell* cell = [tableView dequeueReusableCellWithIdentifier:cellIdent];
    
    if(!cell)
    {
        cell = [[[UITableViewCell alloc] initWithStyle:UITableViewCellStyleSubtitle reuseIdentifier:cellIdent] autorelease];
        [tableView setSeparatorColor:[UIColor blackColor]];
    }
    
    NSObject* obj = [items objectAtIndex:indexPath.row];
    printf("Item requested row %d", indexPath.row);
    
    PSMenuItem* menuItem = (PSMenuItem*)obj;
	
	cell.textLabel.textColor = [UIColor whiteColor];
	cell.textLabel.text = [menuItem title];
	cell.detailTextLabel.text = @"";
    cell.detailTextLabel.textColor = [UIColor whiteColor];
	cell.textLabel.textAlignment = NSTextAlignmentLeft;
	cell.accessoryType = UITableViewCellAccessoryNone;
	cell.backgroundView = nil;

    return cell;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
	//if( self.listDelegate )
	{
		NSObject* item = nil;
		@synchronized(items) {
			item = [items objectAtIndex:indexPath.row];
		}
	    
        // TODO
        //[self.listDelegate listView:self didSelectItem:item];
	}
}

@end
