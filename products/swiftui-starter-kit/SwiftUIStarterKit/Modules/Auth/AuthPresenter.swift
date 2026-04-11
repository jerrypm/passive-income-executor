import Combine

class AuthPresenter: ObservableObject {
    @Published var loginEmail = ""
    @Published var loginPassword = ""
    @Published var registerName = ""
    @Published var registerEmail = ""
    @Published var registerPassword = ""
    @Published var registerConfirmPassword = ""
    @Published var forgotEmail = ""
    @Published var forgotSent = false
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let interactor: AuthInteractorProtocol
    private let onSuccess: () -> Void

    init(interactor: AuthInteractorProtocol, onSuccess: @escaping () -> Void) {
        self.interactor = interactor
        self.onSuccess = onSuccess
    }

    // MARK: - Validation

    var loginEmailError: String? {
        guard !loginEmail.isEmpty else { return nil }
        return loginEmail.isValidEmail ? nil : Strings.invalidEmail
    }

    var loginPasswordError: String? {
        guard !loginPassword.isEmpty else { return nil }
        return loginPassword.count >= AppConstants.minPasswordLength ? nil : Strings.passwordTooShort
    }

    var isLoginValid: Bool {
        loginEmail.isValidEmail && loginPassword.count >= AppConstants.minPasswordLength
    }

    var registerNameError: String? {
        guard !registerName.isEmpty else { return nil }
        return registerName.trimmed.isEmpty ? Strings.nameRequired : nil
    }

    var registerEmailError: String? {
        guard !registerEmail.isEmpty else { return nil }
        return registerEmail.isValidEmail ? nil : Strings.invalidEmail
    }

    var registerPasswordError: String? {
        guard !registerPassword.isEmpty else { return nil }
        return registerPassword.count >= AppConstants.minPasswordLength ? nil : Strings.passwordTooShort
    }

    var registerConfirmError: String? {
        guard !registerConfirmPassword.isEmpty else { return nil }
        return registerConfirmPassword == registerPassword ? nil : Strings.passwordsDontMatch
    }

    var isRegisterValid: Bool {
        !registerName.trimmed.isEmpty
        && registerEmail.isValidEmail
        && registerPassword.count >= AppConstants.minPasswordLength
        && registerConfirmPassword == registerPassword
    }

    var isForgotValid: Bool { forgotEmail.isValidEmail }

    // MARK: - Actions

    @MainActor
    func login() async {
        isLoading = true; errorMessage = nil
        do {
            _ = try await interactor.login(email: loginEmail, password: loginPassword)
            onSuccess()
        } catch { errorMessage = error.localizedDescription }
        isLoading = false
    }

    @MainActor
    func register() async {
        isLoading = true; errorMessage = nil
        do {
            _ = try await interactor.register(name: registerName, email: registerEmail, password: registerPassword)
            onSuccess()
        } catch { errorMessage = error.localizedDescription }
        isLoading = false
    }

    @MainActor
    func forgotPassword() async {
        isLoading = true; errorMessage = nil
        do {
            try await interactor.forgotPassword(email: forgotEmail)
            forgotSent = true
        } catch { errorMessage = error.localizedDescription }
        isLoading = false
    }
}
