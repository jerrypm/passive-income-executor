import SwiftUI

enum ThemeMode: String, CaseIterable {
    case system, light, dark

    var displayName: String {
        switch self {
        case .system: "System"
        case .light: "Light"
        case .dark: "Dark"
        }
    }
}

class ThemeManager: ObservableObject {
    @AppStorage(StorageKeys.selectedTheme) private var selectedTheme = ThemeMode.system.rawValue

    var currentTheme: ThemeMode {
        get { ThemeMode(rawValue: selectedTheme) ?? .system }
        set { selectedTheme = newValue.rawValue; objectWillChange.send() }
    }

    var colorScheme: ColorScheme? {
        switch currentTheme {
        case .system: nil
        case .light: .light
        case .dark: .dark
        }
    }
}
