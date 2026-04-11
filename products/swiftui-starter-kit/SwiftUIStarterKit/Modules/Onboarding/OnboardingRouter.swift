import SwiftUI

enum OnboardingRouter {
    static func createModule(onComplete: @escaping () -> Void) -> some View {
        let interactor = OnboardingInteractor()
        let presenter = OnboardingPresenter(interactor: interactor, onComplete: onComplete)
        return OnboardingView(presenter: presenter)
    }
}
