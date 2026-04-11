import SwiftUI

struct ErrorStateView: View {
    let message: String
    var onRetry: (() -> Void)?

    var body: some View {
        VStack(spacing: AppTheme.spacingMD) {
            Image(systemName: "exclamationmark.triangle")
                .font(.system(size: 56))
                .foregroundStyle(AppColors.error)
            Text(Strings.error)
                .font(AppTheme.headlineFont)
                .foregroundStyle(AppColors.textPrimary)
            Text(message)
                .font(AppTheme.bodyFont)
                .foregroundStyle(AppColors.textSecondary)
                .multilineTextAlignment(.center)
            if let onRetry {
                PrimaryButton(title: Strings.retry, action: onRetry)
                    .padding(.top, AppTheme.spacingSM)
            }
        }
        .padding(AppTheme.spacingXL)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
