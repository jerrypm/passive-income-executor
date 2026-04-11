import SwiftUI

struct TabBarView: View {
    @State private var selectedTab: TabItem = .home
    let onLogout: () -> Void

    var body: some View {
        TabView(selection: $selectedTab) {
            ForEach(TabItem.allCases) { tab in
                tabContent(for: tab)
                    .tabItem {
                        Image(systemName: tab.icon)
                        Text(tab.title)
                    }
                    .tag(tab)
            }
        }
        .tint(AppColors.primary)
    }

    @ViewBuilder
    private func tabContent(for tab: TabItem) -> some View {
        switch tab {
        case .home:
            HomeRouter.createModule()
        case .explore:
            placeholderTab(title: Strings.explore, icon: "magnifyingglass")
        case .profile:
            placeholderTab(title: Strings.profile, icon: "person.fill")
        case .settings:
            SettingsRouter.createModule(onLogout: onLogout)
        }
    }

    private func placeholderTab(title: String, icon: String) -> some View {
        NavigationStack {
            EmptyStateView(icon: icon, title: title, subtitle: Strings.comingSoon)
                .navigationTitle(title)
        }
    }
}
