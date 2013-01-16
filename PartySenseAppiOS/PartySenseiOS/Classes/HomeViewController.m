#import "HomeViewController.h"
#import "PSPageView.h"
#import "MainMenuPageView.h"

@implementation HomeViewController

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    return YES;
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    self.pagingView.currentPageIndex = 0;
    [self currentPageDidChangeInPagingView:self.pagingView];
}


#pragma mark -
#pragma mark ATPagingViewDelegate methods

- (NSInteger)numberOfPagesInPagingView:(ATPagingView *)pagingView {
    return 10;
}

- (UIView *)viewForPageInPagingView:(ATPagingView *)pagingView atIndex:(NSInteger)index {
    
    if(index == 0)
    {
        if(mainMenuPageView == nil)
            mainMenuPageView = [[[MainMenuPageView alloc] init] autorelease];
        
        return mainMenuPageView;
    }
    
    UIView *view = [pagingView dequeueReusablePage];
    if (view == nil) {
        view = [[[PSPageView alloc] init] autorelease];
    }
    return view;
}

- (void)currentPageDidChangeInPagingView:(ATPagingView *)pagingView {
    
    if(pagingView.currentPageIndex == 0)
        self.navigationItem.title = @"Menu";
    else
        self.navigationItem.title = @"NULL";
}


@end
