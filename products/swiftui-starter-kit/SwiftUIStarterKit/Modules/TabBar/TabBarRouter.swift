import SwiftUI

enum TabBarRouter {
    static func createModule(onLogout: @escaping () -> Void) -> some View {
        TabBarView(onLogout: onLogout)
    }
}
