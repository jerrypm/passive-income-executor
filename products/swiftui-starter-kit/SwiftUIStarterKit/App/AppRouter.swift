import SwiftUI

enum AppState: Equatable {
    case onboarding, auth, main
}

class AppRouter: ObservableObject {
    @Published var state: AppState

    init() {
        if !UserDefaultsManager.shared.hasSeenOnboarding {
            state = .onboarding
        } else if KeychainManager.shared.getToken() != nil {
            state = .main
        } else {
            state = .auth
        }
    }

    func completeOnboarding() {
        withAnimation { state = .auth }
    }

    func loginSuccess() {
        withAnimation { state = .main }
    }

    func logout() {
        KeychainManager.shared.deleteToken()
        withAnimation { state = .auth }
    }
}
