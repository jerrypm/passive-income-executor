import SwiftUI

struct LoadingView: View {
    var message: String?

    var body: some View {
        VStack(spacing: AppTheme.spacingMD) {
            ProgressView()
                .controlSize(.large)
            if let message {
                Text(message)
                    .font(AppTheme.captionFont)
                    .foregroundStyle(AppColors.textSecondary)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
