import SwiftUI

struct HomeView: View {
    @ObservedObject var presenter: HomePresenter

    var body: some View {
        NavigationStack {
            Group {
                switch presenter.state {
                case .loading:
                    LoadingView(message: Strings.loading)
                case .loaded(let items):
                    List(items) { item in
                        VStack(alignment: .leading, spacing: AppTheme.spacingXS) {
                            Text(item.title)
                                .font(AppTheme.headlineFont)
                                .foregroundStyle(AppColors.textPrimary)
                            Text(item.subtitle)
                                .font(AppTheme.bodyFont)
                                .foregroundStyle(AppColors.textSecondary)
                        }
                        .padding(.vertical, AppTheme.spacingXS)
                    }
                    .refreshable { await presenter.fetchItems() }
                case .empty:
                    EmptyStateView(
                        icon: "tray", title: Strings.emptyHere,
                        subtitle: Strings.pullToRefresh, buttonTitle: Strings.retry
                    ) { Task { await presenter.fetchItems() } }
                case .error(let message):
                    ErrorStateView(message: message) {
                        Task { await presenter.fetchItems() }
                    }
                }
            }
            .navigationTitle(Strings.home)
        }
        .task { await presenter.fetchItems() }
    }
}
