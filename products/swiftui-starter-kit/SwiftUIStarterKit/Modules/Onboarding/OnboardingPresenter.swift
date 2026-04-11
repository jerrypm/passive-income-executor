import Combine

class OnboardingPresenter: ObservableObject {
    @Published var pages: [OnboardingPage] = []
    @Published var currentPage = 0

    private let interactor: OnboardingInteractorProtocol
    private let onComplete: () -> Void

    var isLastPage: Bool { currentPage == pages.count - 1 }

    init(interactor: OnboardingInteractorProtocol, onComplete: @escaping () -> Void) {
        self.interactor = interactor
        self.onComplete = onComplete
        self.pages = interactor.getPages()
    }

    func nextPage() {
        if isLastPage { complete() }
        else { currentPage += 1 }
    }

    func skip() { complete() }

    private func complete() {
        interactor.completeOnboarding()
        onComplete()
    }
}
