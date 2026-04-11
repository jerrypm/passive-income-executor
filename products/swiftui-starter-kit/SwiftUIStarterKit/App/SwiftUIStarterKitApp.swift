import SwiftUI

@main
struct SwiftUIStarterKitApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate
    @StateObject private var appRouter = AppRouter()
    @StateObject private var themeManager = ThemeManager()

    var body: some Scene {
        WindowGroup {
            Group {
                switch appRouter.state {
                case .onboarding:
                    OnboardingRouter.createModule(onComplete: appRouter.completeOnboarding)
                case .auth:
                    AuthRouter.createModule(onSuccess: appRouter.loginSuccess)
                case .main:
                    TabBarRouter.createModule(onLogout: appRouter.logout)
                }
            }
            .environmentObject(themeManager)
            .preferredColorScheme(themeManager.colorScheme)
            .animation(.easeInOut, value: appRouter.state)
        }
    }
}
