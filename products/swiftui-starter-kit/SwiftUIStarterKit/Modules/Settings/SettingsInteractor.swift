import Foundation

protocol SettingsInteractorProtocol {
    func getUserProfile() -> UserProfile
    func logout()
}

class SettingsInteractor: SettingsInteractorProtocol {
    private let onLogout: () -> Void

    init(onLogout: @escaping () -> Void) {
        self.onLogout = onLogout
    }

    func getUserProfile() -> UserProfile {
        UserProfile(name: "John Doe", email: "john@example.com", avatarURL: nil)
    }

    func logout() {
        KeychainManager.shared.deleteToken()
        onLogout()
    }
}
