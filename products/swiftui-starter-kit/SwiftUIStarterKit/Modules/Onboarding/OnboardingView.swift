import SwiftUI

struct OnboardingView: View {
    @ObservedObject var presenter: OnboardingPresenter

    var body: some View {
        VStack {
            HStack {
                Spacer()
                if !presenter.isLastPage {
                    Button(Strings.skip) { presenter.skip() }
                        .font(AppTheme.bodyFont)
                        .foregroundStyle(AppColors.textSecondary)
                }
            }
            .padding(.horizontal, AppTheme.spacingMD)
            .frame(height: 44)

            TabView(selection: $presenter.currentPage) {
                ForEach(Array(presenter.pages.enumerated()), id: \.element.id) { index, page in
                    VStack(spacing: AppTheme.spacingLG) {
                        Spacer()
                        Image(systemName: page.image)
                            .font(.system(size: 80))
                            .foregroundStyle(AppColors.primary)
                        Text(page.title)
                            .font(AppTheme.titleFont)
                            .foregroundStyle(AppColors.textPrimary)
                        Text(page.subtitle)
                            .font(AppTheme.bodyFont)
                            .foregroundStyle(AppColors.textSecondary)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal, AppTheme.spacingXL)
                        Spacer()
                    }
                    .tag(index)
                }
            }
            .tabViewStyle(.page(indexDisplayMode: .always))

            PrimaryButton(
                title: presenter.isLastPage ? Strings.getStarted : Strings.next
            ) {
                withAnimation { presenter.nextPage() }
            }
            .padding(.horizontal, AppTheme.spacingMD)
            .padding(.bottom, AppTheme.spacingXL)
        }
        .background(AppColors.background)
    }
}
