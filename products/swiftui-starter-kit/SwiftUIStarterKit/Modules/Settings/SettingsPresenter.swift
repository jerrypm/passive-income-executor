import Foundation
import Combine

class SettingsPresenter: ObservableObject {
    @Published var profile: UserProfile
    @Published var notificationsEnabled: Bool

    private let interactor: SettingsInteractorProtocol

    init(interactor: SettingsInteractorProtocol) {
        self.interactor = interactor
        self.profile = interactor.getUserProfile()
        self.notificationsEnabled = UserDefaultsManager.shared.notificationsEnabled
    }

    func toggleNotifications(_ value: Bool) {
        notificationsEnabled = value
        UserDefaultsManager.shared.notificationsEnabled = value
    }

    func logout() { interactor.logout() }

    var appVersion: String {
        Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0"
    }
}
