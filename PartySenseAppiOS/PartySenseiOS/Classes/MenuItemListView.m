//
//  Copyright 2011 Andrey Tarantsov. Distributed under the MIT license.
//

#import "MenuItemListView.h"

@implementation PSMenuItem
@synthesize title;
@end

@implementation MenuItemListView

@synthesize items;
@synthesize listDelegate;

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
    
    [self reloadData];
}

- (NSArray*)items {
    return items;
}

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    // Return the number of sections.
    return 1;
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
    static NSString* cellIdent = @"PartySenseCell";
    UITableViewCell* cell = [tableView dequeueReusableCellWithIdentifier:cellIdent];
    
    if(cell == nil)
    {
        cell = [[[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:cellIdent] autorelease];
        [tableView setSeparatorColor:[UIColor whiteColor]];
    }
    
    NSObject* obj = [items objectAtIndex:indexPath.row];
    printf("\nItem requested row %d", indexPath.row);
    
    PSMenuItem* menuItem = (PSMenuItem*)obj;
	
	cell.textLabel.textColor = [UIColor whiteColor];
	cell.textLabel.text = [menuItem title];
	cell.detailTextLabel.text = @"Blah";
    cell.detailTextLabel.textColor = [UIColor whiteColor];
	cell.textLabel.textAlignment = NSTextAlignmentLeft;
	cell.accessoryType = UITableViewCellAccessoryNone;
	cell.backgroundView = nil;

    return cell;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
	if(listDelegate)
        [listDelegate onItemSelected: indexPath.row];
}

@end
