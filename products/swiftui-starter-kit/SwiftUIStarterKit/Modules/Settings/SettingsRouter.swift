import SwiftUI

enum SettingsRouter {
    static func createModule(onLogout: @escaping () -> Void) -> some View {
        let interactor = SettingsInteractor(onLogout: onLogout)
        let presenter = SettingsPresenter(interactor: interactor)
        return SettingsView(presenter: presenter)
    }
}
