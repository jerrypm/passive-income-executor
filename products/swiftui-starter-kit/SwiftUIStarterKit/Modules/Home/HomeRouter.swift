import SwiftUI

enum HomeRouter {
    static func createModule() -> some View {
        let interactor = HomeInteractor()
        let presenter = HomePresenter(interactor: interactor)
        return HomeView(presenter: presenter)
    }
}
