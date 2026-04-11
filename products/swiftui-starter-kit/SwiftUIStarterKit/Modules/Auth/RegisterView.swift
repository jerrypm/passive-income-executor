import SwiftUI

struct RegisterView: View {
    @ObservedObject var presenter: AuthPresenter

    var body: some View {
        ScrollView {
            VStack(spacing: AppTheme.spacingMD) {
                Spacer().frame(height: AppTheme.spacingLG)

                Text(Strings.register)
                    .font(AppTheme.titleFont)
                    .foregroundStyle(AppColors.textPrimary)

                InputField(label: Strings.name, text: $presenter.registerName, placeholder: "John Doe", error: presenter.registerNameError)
                InputField(label: Strings.email, text: $presenter.registerEmail, placeholder: "john@example.com", error: presenter.registerEmailError, keyboardType: .emailAddress)
                InputField(label: Strings.password, text: $presenter.registerPassword, placeholder: "********", isSecure: true, error: presenter.registerPasswordError)
                InputField(label: Strings.confirmPassword, text: $presenter.registerConfirmPassword, placeholder: "********", isSecure: true, error: presenter.registerConfirmError)

                if let error = presenter.errorMessage {
                    Text(error).font(AppTheme.captionFont).foregroundStyle(AppColors.error)
                }

                PrimaryButton(
                    title: Strings.register,
                    isLoading: presenter.isLoading,
                    isDisabled: !presenter.isRegisterValid
                ) { Task { await presenter.register() } }

                NavigationLink {
                    LoginView(presenter: presenter)
                } label: {
                    Text(Strings.alreadyHaveAccount)
                        .font(AppTheme.bodyFont)
                        .foregroundStyle(AppColors.textSecondary)
                }
                .padding(.top, AppTheme.spacingSM)
            }
            .padding(.horizontal, AppTheme.spacingMD)
        }
        .background(AppColors.background)
        .onTapGesture { hideKeyboard() }
        .navigationBarTitleDisplayMode(.inline)
    }
}
