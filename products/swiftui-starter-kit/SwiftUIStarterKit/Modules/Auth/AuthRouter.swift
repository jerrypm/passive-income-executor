import SwiftUI

enum AuthRouter {
    static func createModule(onSuccess: @escaping () -> Void) -> some View {
        let interactor = AuthInteractor()
        let presenter = AuthPresenter(interactor: interactor, onSuccess: onSuccess)
        return NavigationStack {
            LoginView(presenter: presenter)
        }
    }
}
