import SwiftUI

struct LoginView: View {
    @ObservedObject var presenter: AuthPresenter

    var body: some View {
        ScrollView {
            VStack(spacing: AppTheme.spacingMD) {
                Spacer().frame(height: AppTheme.spacingXL)

                Text(Strings.login)
                    .font(AppTheme.titleFont)
                    .foregroundStyle(AppColors.textPrimary)

                InputField(
                    label: Strings.email, text: $presenter.loginEmail,
                    placeholder: "john@example.com",
                    error: presenter.loginEmailError, keyboardType: .emailAddress
                )
                InputField(
                    label: Strings.password, text: $presenter.loginPassword,
                    placeholder: "********", isSecure: true,
                    error: presenter.loginPasswordError
                )

                NavigationLink {
                    ForgotPasswordView(presenter: presenter)
                } label: {
                    Text(Strings.forgotPassword)
                        .font(AppTheme.captionFont)
                        .foregroundStyle(AppColors.primary)
                        .frame(maxWidth: .infinity, alignment: .trailing)
                }

                if let error = presenter.errorMessage {
                    Text(error).font(AppTheme.captionFont).foregroundStyle(AppColors.error)
                }

                PrimaryButton(
                    title: Strings.login,
                    isLoading: presenter.isLoading,
                    isDisabled: !presenter.isLoginValid
                ) { Task { await presenter.login() } }

                NavigationLink {
                    RegisterView(presenter: presenter)
                } label: {
                    Text(Strings.dontHaveAccount)
                        .font(AppTheme.bodyFont)
                        .foregroundStyle(AppColors.textSecondary)
                }
                .padding(.top, AppTheme.spacingSM)
            }
            .padding(.horizontal, AppTheme.spacingMD)
        }
        .background(AppColors.background)
        .onTapGesture { hideKeyboard() }
    }
}
