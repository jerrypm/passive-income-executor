import Foundation

class UserDefaultsManager {
    static let shared = UserDefaultsManager()
    private let defaults = UserDefaults.standard
    private init() {}

    var hasSeenOnboarding: Bool {
        get { defaults.bool(forKey: StorageKeys.hasSeenOnboarding) }
        set { defaults.set(newValue, forKey: StorageKeys.hasSeenOnboarding) }
    }

    var notificationsEnabled: Bool {
        get { defaults.bool(forKey: StorageKeys.notificationsEnabled) }
        set { defaults.set(newValue, forKey: StorageKeys.notificationsEnabled) }
    }
}
