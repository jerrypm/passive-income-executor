import SwiftUI

struct EmptyStateView: View {
    let icon: String
    let title: String
    let subtitle: String
    var buttonTitle: String?
    var onAction: (() -> Void)?

    var body: some View {
        VStack(spacing: AppTheme.spacingMD) {
            Image(systemName: icon)
                .font(.system(size: 56))
                .foregroundStyle(AppColors.textSecondary)
            Text(title)
                .font(AppTheme.headlineFont)
                .foregroundStyle(AppColors.textPrimary)
            Text(subtitle)
                .font(AppTheme.bodyFont)
                .foregroundStyle(AppColors.textSecondary)
                .multilineTextAlignment(.center)
            if let buttonTitle, let onAction {
                PrimaryButton(title: buttonTitle, action: onAction)
                    .padding(.top, AppTheme.spacingSM)
            }
        }
        .padding(AppTheme.spacingXL)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
