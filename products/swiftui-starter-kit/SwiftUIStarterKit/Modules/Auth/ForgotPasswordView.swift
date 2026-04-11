import SwiftUI

struct ForgotPasswordView: View {
    @ObservedObject var presenter: AuthPresenter

    var body: some View {
        VStack(spacing: AppTheme.spacingMD) {
            Spacer()

            if presenter.forgotSent {
                Image(systemName: "envelope.badge.fill")
                    .font(.system(size: 56))
                    .foregroundStyle(AppColors.primary)
                Text(Strings.resetLinkSent)
                    .font(AppTheme.headlineFont)
                    .foregroundStyle(AppColors.textPrimary)
                    .multilineTextAlignment(.center)
            } else {
                Text(Strings.forgotPassword)
                    .font(AppTheme.titleFont)
                    .foregroundStyle(AppColors.textPrimary)

                InputField(label: Strings.email, text: $presenter.forgotEmail, placeholder: "john@example.com", keyboardType: .emailAddress)

                if let error = presenter.errorMessage {
                    Text(error).font(AppTheme.captionFont).foregroundStyle(AppColors.error)
                }

                PrimaryButton(
                    title: Strings.sendResetLink,
                    isLoading: presenter.isLoading,
                    isDisabled: !presenter.isForgotValid
                ) { Task { await presenter.forgotPassword() } }
            }

            Spacer()
        }
        .padding(.horizontal, AppTheme.spacingMD)
        .background(AppColors.background)
        .onTapGesture { hideKeyboard() }
        .navigationBarTitleDisplayMode(.inline)
    }
}
