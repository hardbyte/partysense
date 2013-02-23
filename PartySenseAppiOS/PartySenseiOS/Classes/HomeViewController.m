#import "HomeViewController.h"
#import "PSPageView.h"
#import "MainMenuPageView.h"
#import "PSCentral.h"
#import "RecommendedClubsPageView.h"
#import "NearbyClubsPageView.h"

@implementation HomeViewController

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    return YES;
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    self.pagingView.currentPageIndex = 0;
    [self currentPageDidChangeInPagingView: self.pagingView];
}

#pragma mark -
#pragma mark ATPagingViewDelegate methods

- (void)loadView {
    
    
    [super loadView];

    UIImage* headerBg = [UIImage imageNamed:@"Data/header_bg.png"];
    UIImage* navBackground =[headerBg resizableImageWithCapInsets:UIEdgeInsetsMake(0, 0, 0, 0)];
    [self.navigationController.navigationBar setBackgroundImage: navBackground forBarMetrics: UIBarMetricsDefault];
}

- (NSInteger)numberOfPagesInPagingView:(ATPagingView *)pagingView {
    return 2;
}

- (UIView *)viewForPageInPagingView:(ATPagingView *)pagingView atIndex:(NSInteger)index {
    
    if(index == 0)
    {
        if(mainMenuPageView == nil)
        {
            mainMenuPageView = [[[MainMenuPageView alloc] initWithFrame: [pagingView bounds]] autorelease];
            mainMenuPageView.pagingView = self.pagingView;
            mainMenuPageView.delegate = self;
        }
        
        return mainMenuPageView;
    }
    else
    {
        switch (selectedIndex) {
            case 0:
                if(recommendedPageView == nil)
                {
                    recommendedPageView = [[[RecommendedClubsPageView alloc] initWithFrame: [pagingView bounds]] autorelease];
                    recommendedPageView.pagingView = self.pagingView;
                }
                
                return recommendedPageView;
            case 1:
                if(nearbyPageView == nil)
                {
                    nearbyPageView = [[[NearbyClubsPageView alloc] initWithFrame: [pagingView bounds]] autorelease];
                    nearbyPageView.pagingView = self.pagingView;
                }
                
                return nearbyPageView;

            default:
                break;
        }
        
    }
    
    PSPageView* view = (PSPageView*)[pagingView dequeueReusablePage];
    if (view == nil)
    {
        view = [[[PSPageView alloc] init] autorelease];
        view.title = pageStrings[index];
    }
    
    return view;
}

- (void)onPageSelected:(NSInteger)index
{
    selectedIndex = index;
    self.pagingView.currentPageIndex = 1;
}

- (void)currentPageDidChangeInPagingView:(ATPagingView *)pagingView
{
    if(pagingView.currentPageIndex == 0)
        self.navigationItem.title = @"PartySense";
    else
        self.navigationItem.title = [currentPageView title];
}


@end
