import Foundation

enum TabItem: Int, CaseIterable, Identifiable {
    case home, explore, profile, settings

    var id: Int { rawValue }

    var title: String {
        switch self {
        case .home: Strings.home
        case .explore: Strings.explore
        case .profile: Strings.profile
        case .settings: Strings.settings
        }
    }

    var icon: String {
        switch self {
        case .home: "house.fill"
        case .explore: "magnifyingglass"
        case .profile: "person.fill"
        case .settings: "gearshape.fill"
        }
    }
}
