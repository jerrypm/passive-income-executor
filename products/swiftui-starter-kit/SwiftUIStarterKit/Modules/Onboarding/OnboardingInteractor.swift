import Foundation

protocol OnboardingInteractorProtocol {
    func getPages() -> [OnboardingPage]
    func completeOnboarding()
}

class OnboardingInteractor: OnboardingInteractorProtocol {
    func getPages() -> [OnboardingPage] {
        [
            OnboardingPage(image: "star.fill", title: Strings.onboardingTitle1, subtitle: Strings.onboardingSubtitle1),
            OnboardingPage(image: "bolt.fill", title: Strings.onboardingTitle2, subtitle: Strings.onboardingSubtitle2),
            OnboardingPage(image: "heart.fill", title: Strings.onboardingTitle3, subtitle: Strings.onboardingSubtitle3),
        ]
    }

    func completeOnboarding() {
        UserDefaultsManager.shared.hasSeenOnboarding = true
    }
}
