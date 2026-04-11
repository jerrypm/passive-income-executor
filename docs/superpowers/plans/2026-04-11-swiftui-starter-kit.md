# SwiftUI Starter Kit — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete SwiftUI VIPER boilerplate Xcode project to sell on Gumroad for $29.

**Architecture:** Single Xcode project using VIPER (Router → Interactor → Presenter → View → Entity). Each module follows the same pattern: Router wires dependencies, Interactor handles business logic, Presenter is an ObservableObject with @Published state, View observes Presenter, Entity defines data models. Max 200 lines per file, 1 type per file.

**Tech Stack:** Swift 5.9+, SwiftUI, iOS 17+ / iPadOS 17+, Xcode 16+, zero third-party dependencies. XcodeGen for project generation.

**Spec:** `docs/superpowers/specs/2026-04-11-swiftui-starter-kit-design.md`

**Base path:** `products/swiftui-starter-kit`
**Source path:** `products/swiftui-starter-kit/SwiftUIStarterKit`

---

## File Map

```
products/swiftui-starter-kit/
├── project.yml                                          # XcodeGen config
├── SwiftUIStarterKit/
│   ├── App/
│   │   ├── SwiftUIStarterKitApp.swift                   # @main entry point
│   │   ├── AppDelegate.swift                            # Push notification handling
│   │   └── AppRouter.swift                              # Root navigation coordinator
│   ├── Core/
│   │   ├── Network/
│   │   │   ├── APIClient.swift                          # Generic async/await HTTP client
│   │   │   ├── APIEndpoint.swift                        # Endpoint protocol + HTTPMethod
│   │   │   ├── APIError.swift                           # Typed error enum
│   │   │   └── MockAPIClient.swift                      # Mock for previews/testing
│   │   ├── Storage/
│   │   │   ├── KeychainManager.swift                    # Keychain wrapper (Security framework)
│   │   │   └── UserDefaultsManager.swift                # App preferences
│   │   ├── Theme/
│   │   │   ├── AppColors.swift                          # Semantic color references
│   │   │   ├── AppTheme.swift                           # Fonts, spacing, corner radius
│   │   │   └── ThemeManager.swift                       # Dark/light/system toggle
│   │   ├── Notifications/
│   │   │   └── NotificationManager.swift                # Push permission + token
│   │   └── Localization/
│   │       ├── en.lproj/Localizable.strings             # English strings
│   │       └── id.lproj/Localizable.strings             # Indonesian strings
│   ├── Modules/
│   │   ├── Onboarding/
│   │   │   ├── OnboardingEntity.swift
│   │   │   ├── OnboardingInteractor.swift
│   │   │   ├── OnboardingPresenter.swift
│   │   │   ├── OnboardingView.swift
│   │   │   └── OnboardingRouter.swift
│   │   ├── Auth/
│   │   │   ├── AuthEntity.swift                         # User, AuthResponse, endpoints
│   │   │   ├── AuthInteractor.swift
│   │   │   ├── AuthPresenter.swift
│   │   │   ├── LoginView.swift
│   │   │   ├── RegisterView.swift
│   │   │   ├── ForgotPasswordView.swift
│   │   │   └── AuthRouter.swift
│   │   ├── Home/
│   │   │   ├── HomeEntity.swift
│   │   │   ├── HomeInteractor.swift
│   │   │   ├── HomePresenter.swift
│   │   │   ├── HomeView.swift
│   │   │   └── HomeRouter.swift
│   │   ├── Settings/
│   │   │   ├── SettingsEntity.swift
│   │   │   ├── SettingsInteractor.swift
│   │   │   ├── SettingsPresenter.swift
│   │   │   ├── SettingsView.swift
│   │   │   └── SettingsRouter.swift
│   │   └── TabBar/
│   │       ├── TabBarEntity.swift
│   │       ├── TabBarView.swift
│   │       └── TabBarRouter.swift
│   ├── SharedUI/
│   │   ├── LoadingView.swift
│   │   ├── EmptyStateView.swift
│   │   ├── ErrorStateView.swift
│   │   ├── PrimaryButton.swift
│   │   ├── InputField.swift
│   │   └── AvatarView.swift
│   ├── Extensions/
│   │   ├── View+Extensions.swift
│   │   ├── Color+Extensions.swift
│   │   └── String+Extensions.swift
│   ├── Constants/
│   │   ├── AppConstants.swift
│   │   ├── StorageKeys.swift
│   │   └── Strings.swift
│   └── Resources/
│       └── Assets.xcassets/                             # Color assets + app icon
├── README.md
├── CUSTOMIZATION.md
├── ARCHITECTURE.md
├── LICENSE
└── gumroad-listing.md
```

---

### Task 1: Project Scaffold + XcodeGen

**Files:**
- Create: `products/swiftui-starter-kit/project.yml`
- Create: `products/swiftui-starter-kit/SwiftUIStarterKit/App/SwiftUIStarterKitApp.swift` (minimal placeholder)

- [ ] **Step 1: Install xcodegen if not available**

```bash
which xcodegen || brew install xcodegen
```

- [ ] **Step 2: Create directory structure**

```bash
BASE="products/swiftui-starter-kit"
mkdir -p "$BASE/SwiftUIStarterKit/App"
mkdir -p "$BASE/SwiftUIStarterKit/Core/Network"
mkdir -p "$BASE/SwiftUIStarterKit/Core/Storage"
mkdir -p "$BASE/SwiftUIStarterKit/Core/Theme"
mkdir -p "$BASE/SwiftUIStarterKit/Core/Notifications"
mkdir -p "$BASE/SwiftUIStarterKit/Core/Localization/en.lproj"
mkdir -p "$BASE/SwiftUIStarterKit/Core/Localization/id.lproj"
mkdir -p "$BASE/SwiftUIStarterKit/Modules/Onboarding"
mkdir -p "$BASE/SwiftUIStarterKit/Modules/Auth"
mkdir -p "$BASE/SwiftUIStarterKit/Modules/Home"
mkdir -p "$BASE/SwiftUIStarterKit/Modules/Settings"
mkdir -p "$BASE/SwiftUIStarterKit/Modules/TabBar"
mkdir -p "$BASE/SwiftUIStarterKit/SharedUI"
mkdir -p "$BASE/SwiftUIStarterKit/Extensions"
mkdir -p "$BASE/SwiftUIStarterKit/Constants"
mkdir -p "$BASE/SwiftUIStarterKit/Resources/Assets.xcassets/AccentColor.colorset"
mkdir -p "$BASE/SwiftUIStarterKit/Resources/Assets.xcassets/AppIcon.appiconset"
mkdir -p "$BASE/SwiftUIStarterKit/Resources/Assets.xcassets/Colors/Primary.colorset"
mkdir -p "$BASE/SwiftUIStarterKit/Resources/Assets.xcassets/Colors/Secondary.colorset"
mkdir -p "$BASE/SwiftUIStarterKit/Resources/Assets.xcassets/Colors/Background.colorset"
mkdir -p "$BASE/SwiftUIStarterKit/Resources/Assets.xcassets/Colors/Surface.colorset"
mkdir -p "$BASE/SwiftUIStarterKit/Resources/Assets.xcassets/Colors/Error.colorset"
mkdir -p "$BASE/SwiftUIStarterKit/Resources/Assets.xcassets/Colors/TextPrimary.colorset"
mkdir -p "$BASE/SwiftUIStarterKit/Resources/Assets.xcassets/Colors/TextSecondary.colorset"
```

- [ ] **Step 3: Create project.yml**

Write to `products/swiftui-starter-kit/project.yml`:

```yaml
name: SwiftUIStarterKit
options:
  bundleIdPrefix: com.example
  deploymentTarget:
    iOS: "17.0"
  createIntermediateGroups: true
settings:
  SWIFT_VERSION: "5.9"
  MARKETING_VERSION: "1.0.0"
  CURRENT_PROJECT_VERSION: 1
targets:
  SwiftUIStarterKit:
    type: application
    platform: iOS
    sources:
      - path: SwiftUIStarterKit
    settings:
      GENERATE_INFOPLIST_FILE: true
      INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents: true
      INFOPLIST_KEY_UILaunchScreen_Generation: true
      INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone: UIInterfaceOrientationPortrait
      INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad: "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight"
      TARGETED_DEVICE_FAMILY: "1,2"
      SUPPORTS_MAC_DESIGNED_FOR_IPHONE: false
schemes:
  SwiftUIStarterKit:
    build:
      targets:
        SwiftUIStarterKit: all
    run:
      config: Debug
```

- [ ] **Step 4: Create minimal App entry point (placeholder)**

Write to `products/swiftui-starter-kit/SwiftUIStarterKit/App/SwiftUIStarterKitApp.swift`:

```swift
import SwiftUI

@main
struct SwiftUIStarterKitApp: App {
    var body: some Scene {
        WindowGroup {
            Text("SwiftUI Starter Kit")
        }
    }
}
```

- [ ] **Step 5: Generate Xcode project and verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

Expected: BUILD SUCCEEDED

- [ ] **Step 6: Commit**

```bash
git add products/swiftui-starter-kit/
git commit -m "feat(swiftui-starter-kit): scaffold project with xcodegen"
```

---

### Task 2: Constants + StorageKeys + Extensions

**Files:**
- Create: `SwiftUIStarterKit/Constants/AppConstants.swift`
- Create: `SwiftUIStarterKit/Constants/StorageKeys.swift`
- Create: `SwiftUIStarterKit/Extensions/View+Extensions.swift`
- Create: `SwiftUIStarterKit/Extensions/Color+Extensions.swift`
- Create: `SwiftUIStarterKit/Extensions/String+Extensions.swift`

All paths below relative to `products/swiftui-starter-kit/`.

- [ ] **Step 1: Create AppConstants.swift**

```swift
import Foundation

enum AppConstants {
    static let apiBaseURL = "https://api.example.com/v1"
    static let appName = "SwiftUI Starter Kit"
    static let minPasswordLength = 8
}
```

- [ ] **Step 2: Create StorageKeys.swift**

```swift
import Foundation

enum StorageKeys {
    static let authToken = "auth_token"
    static let refreshToken = "refresh_token"
    static let hasSeenOnboarding = "has_seen_onboarding"
    static let selectedTheme = "selected_theme"
    static let notificationsEnabled = "notifications_enabled"
}
```

- [ ] **Step 3: Create View+Extensions.swift**

```swift
import SwiftUI

extension View {
    func hideKeyboard() {
        UIApplication.shared.sendAction(
            #selector(UIResponder.resignFirstResponder),
            to: nil, from: nil, for: nil
        )
    }
}
```

- [ ] **Step 4: Create Color+Extensions.swift**

```swift
import SwiftUI

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 6: (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default: (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(.sRGB, red: Double(r) / 255, green: Double(g) / 255, blue: Double(b) / 255, opacity: Double(a) / 255)
    }
}
```

- [ ] **Step 5: Create String+Extensions.swift**

```swift
import Foundation

extension String {
    var isValidEmail: Bool {
        let regex = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}"
        return NSPredicate(format: "SELF MATCHES %@", regex).evaluate(with: self)
    }

    var trimmed: String {
        trimmingCharacters(in: .whitespacesAndNewlines)
    }
}
```

- [ ] **Step 6: Regenerate project + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 7: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Constants/ products/swiftui-starter-kit/SwiftUIStarterKit/Extensions/
git commit -m "feat(swiftui-starter-kit): add constants and extensions"
```

---

### Task 3: Theme System + Color Assets

**Files:**
- Create: `SwiftUIStarterKit/Core/Theme/AppColors.swift`
- Create: `SwiftUIStarterKit/Core/Theme/AppTheme.swift`
- Create: `SwiftUIStarterKit/Core/Theme/ThemeManager.swift`
- Create: `SwiftUIStarterKit/Resources/Assets.xcassets/` color set JSON files

- [ ] **Step 1: Create all color asset Contents.json files**

Run this script from `products/swiftui-starter-kit/`:

```bash
#!/bin/bash
BASE="SwiftUIStarterKit/Resources/Assets.xcassets"

# Root Contents.json
cat > "$BASE/Contents.json" << 'EOF'
{ "info" : { "author" : "xcode", "version" : 1 } }
EOF

cat > "$BASE/Colors/Contents.json" << 'EOF'
{ "info" : { "author" : "xcode", "version" : 1 }, "properties" : { "provides-namespace" : true } }
EOF

# AccentColor = same as Primary
create_color() {
    local NAME=$1 LR=$2 LG=$3 LB=$4 DR=$5 DG=$6 DB=$7
    cat > "$BASE/Colors/$NAME.colorset/Contents.json" << EOFCOLOR
{
  "colors" : [
    { "color" : { "color-space" : "srgb", "components" : { "red" : "$LR", "green" : "$LG", "blue" : "$LB", "alpha" : "1.000" } }, "idiom" : "universal" },
    { "appearances" : [ { "appearance" : "luminosity", "value" : "dark" } ], "color" : { "color-space" : "srgb", "components" : { "red" : "$DR", "green" : "$DG", "blue" : "$DB", "alpha" : "1.000" } }, "idiom" : "universal" }
  ],
  "info" : { "author" : "xcode", "version" : 1 }
}
EOFCOLOR
}

create_color "Primary"       "0.220" "0.478" "1.000"   "0.380" "0.580" "1.000"
create_color "Secondary"     "0.545" "0.361" "0.965"   "0.655" "0.545" "0.980"
create_color "Background"    "1.000" "1.000" "1.000"   "0.110" "0.110" "0.118"
create_color "Surface"       "0.949" "0.949" "0.969"   "0.173" "0.173" "0.180"
create_color "Error"         "1.000" "0.231" "0.188"   "1.000" "0.412" "0.380"
create_color "TextPrimary"   "0.110" "0.110" "0.118"   "0.949" "0.949" "0.969"
create_color "TextSecondary" "0.557" "0.557" "0.576"   "0.682" "0.682" "0.698"

# AccentColor
cat > "$BASE/AccentColor.colorset/Contents.json" << 'EOF'
{
  "colors" : [
    { "color" : { "color-space" : "srgb", "components" : { "red" : "0.220", "green" : "0.478", "blue" : "1.000", "alpha" : "1.000" } }, "idiom" : "universal" }
  ],
  "info" : { "author" : "xcode", "version" : 1 }
}
EOF

# AppIcon (empty placeholder)
cat > "$BASE/AppIcon.appiconset/Contents.json" << 'EOF'
{ "images" : [ { "idiom" : "universal", "platform" : "ios", "size" : "1024x1024" } ], "info" : { "author" : "xcode", "version" : 1 } }
EOF
```

- [ ] **Step 2: Create AppColors.swift**

```swift
import SwiftUI

enum AppColors {
    static let primary = Color("Primary")
    static let secondary = Color("Secondary")
    static let background = Color("Background")
    static let surface = Color("Surface")
    static let error = Color("Error")
    static let textPrimary = Color("TextPrimary")
    static let textSecondary = Color("TextSecondary")
}
```

- [ ] **Step 3: Create AppTheme.swift**

```swift
import SwiftUI

enum AppTheme {
    static let titleFont = Font.system(size: 28, weight: .bold)
    static let headlineFont = Font.system(size: 20, weight: .semibold)
    static let bodyFont = Font.system(size: 16, weight: .regular)
    static let captionFont = Font.system(size: 14, weight: .regular)
    static let buttonFont = Font.system(size: 16, weight: .semibold)

    static let spacingXS: CGFloat = 4
    static let spacingSM: CGFloat = 8
    static let spacingMD: CGFloat = 16
    static let spacingLG: CGFloat = 24
    static let spacingXL: CGFloat = 32

    static let cornerRadiusSM: CGFloat = 8
    static let cornerRadiusMD: CGFloat = 12
    static let cornerRadiusLG: CGFloat = 16
}
```

- [ ] **Step 4: Create ThemeManager.swift**

```swift
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
```

- [ ] **Step 5: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 6: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Core/Theme/ products/swiftui-starter-kit/SwiftUIStarterKit/Resources/
git commit -m "feat(swiftui-starter-kit): add theme system and color assets"
```

---

### Task 4: Storage Layer

**Files:**
- Create: `SwiftUIStarterKit/Core/Storage/KeychainManager.swift`
- Create: `SwiftUIStarterKit/Core/Storage/UserDefaultsManager.swift`

- [ ] **Step 1: Create KeychainManager.swift**

```swift
import Foundation
import Security

class KeychainManager {
    static let shared = KeychainManager()
    private init() {}

    func save(_ value: String, forKey key: String) {
        guard let data = value.data(using: .utf8) else { return }
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]
        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, nil)
    }

    func get(forKey key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]
        var result: AnyObject?
        SecItemCopyMatching(query as CFDictionary, &result)
        guard let data = result as? Data else { return nil }
        return String(data: data, encoding: .utf8)
    }

    func delete(forKey key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]
        SecItemDelete(query as CFDictionary)
    }

    func getToken() -> String? { get(forKey: StorageKeys.authToken) }
    func saveToken(_ token: String) { save(token, forKey: StorageKeys.authToken) }
    func deleteToken() { delete(forKey: StorageKeys.authToken) }
}
```

- [ ] **Step 2: Create UserDefaultsManager.swift**

```swift
import Foundation

class UserDefaultsManager {
    static let shared = UserDefaultsManager()
    private let defaults = UserDefaults.standard
    private init() {}

    var hasSeenOnboarding: Bool {
        get { defaults.bool(forKey: StorageKeys.hasSeenOnboarding) }
        set { defaults.set(newValue, forKey: StorageKeys.hasSeenOnboarding) }
    }

    var notificationsEnabled: Bool {
        get { defaults.bool(forKey: StorageKeys.notificationsEnabled) }
        set { defaults.set(newValue, forKey: StorageKeys.notificationsEnabled) }
    }
}
```

- [ ] **Step 3: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 4: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Core/Storage/
git commit -m "feat(swiftui-starter-kit): add keychain and user defaults managers"
```

---

### Task 5: Network Layer

**Files:**
- Create: `SwiftUIStarterKit/Core/Network/APIError.swift`
- Create: `SwiftUIStarterKit/Core/Network/APIEndpoint.swift`
- Create: `SwiftUIStarterKit/Core/Network/APIClient.swift`
- Create: `SwiftUIStarterKit/Core/Network/MockAPIClient.swift`

- [ ] **Step 1: Create APIError.swift**

```swift
import Foundation

enum APIError: LocalizedError {
    case unauthorized
    case notFound
    case serverError(Int)
    case noConnection
    case decodingError
    case custom(String)

    var errorDescription: String? {
        switch self {
        case .unauthorized: "Unauthorized"
        case .notFound: "Resource not found"
        case .serverError(let code): "Server error (\(code))"
        case .noConnection: "No internet connection"
        case .decodingError: "Failed to decode response"
        case .custom(let msg): msg
        }
    }
}
```

- [ ] **Step 2: Create APIEndpoint.swift**

```swift
import Foundation

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case delete = "DELETE"
}

protocol APIEndpoint {
    var path: String { get }
    var method: HTTPMethod { get }
    var body: Data? { get }
    var queryItems: [URLQueryItem]? { get }
}

extension APIEndpoint {
    var body: Data? { nil }
    var queryItems: [URLQueryItem]? { nil }

    var url: URL? {
        var components = URLComponents(string: AppConstants.apiBaseURL + path)
        components?.queryItems = queryItems
        return components?.url
    }
}
```

- [ ] **Step 3: Create APIClient.swift**

```swift
import Foundation

protocol APIClientProtocol {
    func request<T: Decodable>(_ endpoint: APIEndpoint) async throws -> T
}

class APIClient: APIClientProtocol {
    static let shared = APIClient()
    private let session: URLSession
    private let decoder: JSONDecoder

    init(session: URLSession = .shared) {
        self.session = session
        self.decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
    }

    func request<T: Decodable>(_ endpoint: APIEndpoint) async throws -> T {
        guard let url = endpoint.url else {
            throw APIError.custom("Invalid URL")
        }

        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.httpBody = endpoint.body

        if endpoint.body != nil {
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        }
        if let token = KeychainManager.shared.getToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        let data: Data
        let response: URLResponse
        do {
            (data, response) = try await session.data(for: request)
        } catch {
            throw APIError.noConnection
        }

        guard let http = response as? HTTPURLResponse else {
            throw APIError.serverError(0)
        }

        switch http.statusCode {
        case 200...299:
            do { return try decoder.decode(T.self, from: data) }
            catch { throw APIError.decodingError }
        case 401: throw APIError.unauthorized
        case 404: throw APIError.notFound
        default: throw APIError.serverError(http.statusCode)
        }
    }
}
```

- [ ] **Step 4: Create MockAPIClient.swift**

```swift
import Foundation

class MockAPIClient: APIClientProtocol {
    static let shared = MockAPIClient()

    func request<T: Decodable>(_ endpoint: APIEndpoint) async throws -> T {
        try await Task.sleep(for: .seconds(0.5))

        let json: String
        switch endpoint.path {
        case "/auth/login", "/auth/register":
            json = """
            {"token":"mock_jwt_token_12345","user":{"id":"1","name":"John Doe","email":"john@example.com"}}
            """
        case "/auth/forgot-password":
            json = """
            {"message":"Reset link sent"}
            """
        case "/items":
            json = """
            [
              {"id":"1","title":"First Item","subtitle":"Description of the first item"},
              {"id":"2","title":"Second Item","subtitle":"Description of the second item"},
              {"id":"3","title":"Third Item","subtitle":"Description of the third item"},
              {"id":"4","title":"Fourth Item","subtitle":"Description of the fourth item"},
              {"id":"5","title":"Fifth Item","subtitle":"Description of the fifth item"}
            ]
            """
        default:
            json = "{}"
        }

        guard let data = json.data(using: .utf8) else { throw APIError.decodingError }
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(T.self, from: data)
    }
}
```

- [ ] **Step 5: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 6: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Core/Network/
git commit -m "feat(swiftui-starter-kit): add network layer with mock API client"
```

---

### Task 6: Localization + Strings

**Files:**
- Create: `SwiftUIStarterKit/Core/Localization/en.lproj/Localizable.strings`
- Create: `SwiftUIStarterKit/Core/Localization/id.lproj/Localizable.strings`
- Create: `SwiftUIStarterKit/Constants/Strings.swift`

- [ ] **Step 1: Create en.lproj/Localizable.strings**

```
/* General */
"app_name" = "SwiftUI Starter Kit";
"ok" = "OK";
"cancel" = "Cancel";
"error" = "Error";
"retry" = "Retry";
"loading" = "Loading...";

/* Onboarding */
"onboarding_title_1" = "Welcome";
"onboarding_subtitle_1" = "Discover a new way to build amazing apps with SwiftUI.";
"onboarding_title_2" = "Fast & Powerful";
"onboarding_subtitle_2" = "Built with VIPER architecture for scalable and testable code.";
"onboarding_title_3" = "Get Started";
"onboarding_subtitle_3" = "Everything you need to launch your next iOS app.";
"skip" = "Skip";
"next" = "Next";
"get_started" = "Get Started";

/* Auth */
"login" = "Log In";
"register" = "Sign Up";
"email" = "Email";
"password" = "Password";
"confirm_password" = "Confirm Password";
"name" = "Full Name";
"forgot_password" = "Forgot Password?";
"dont_have_account" = "Don't have an account? Sign Up";
"already_have_account" = "Already have an account? Log In";
"send_reset_link" = "Send Reset Link";
"reset_link_sent" = "Check your email for the password reset link.";

/* Validation */
"invalid_email" = "Please enter a valid email address";
"password_too_short" = "Password must be at least 8 characters";
"passwords_dont_match" = "Passwords don't match";
"name_required" = "Name is required";

/* Tabs & Home */
"home" = "Home";
"explore" = "Explore";
"profile" = "Profile";
"no_items" = "No items yet";
"pull_to_refresh" = "Pull to refresh or tap retry";

/* Settings */
"settings" = "Settings";
"notifications" = "Notifications";
"theme" = "Theme";
"language" = "Language";
"about" = "About";
"version" = "Version";
"terms_of_service" = "Terms of Service";
"privacy_policy" = "Privacy Policy";
"logout" = "Log Out";
"dark" = "Dark";
"light" = "Light";
"system" = "System";

/* States */
"something_went_wrong" = "Something went wrong";
"no_connection" = "No internet connection";
"empty_here" = "Nothing here yet";
"coming_soon" = "Coming soon";
```

- [ ] **Step 2: Create id.lproj/Localizable.strings**

```
/* General */
"app_name" = "SwiftUI Starter Kit";
"ok" = "OK";
"cancel" = "Batal";
"error" = "Kesalahan";
"retry" = "Coba Lagi";
"loading" = "Memuat...";

/* Onboarding */
"onboarding_title_1" = "Selamat Datang";
"onboarding_subtitle_1" = "Temukan cara baru membangun aplikasi luar biasa dengan SwiftUI.";
"onboarding_title_2" = "Cepat & Powerful";
"onboarding_subtitle_2" = "Dibangun dengan arsitektur VIPER untuk kode yang scalable dan testable.";
"onboarding_title_3" = "Mulai Sekarang";
"onboarding_subtitle_3" = "Semua yang kamu butuhkan untuk meluncurkan aplikasi iOS berikutnya.";
"skip" = "Lewati";
"next" = "Lanjut";
"get_started" = "Mulai";

/* Auth */
"login" = "Masuk";
"register" = "Daftar";
"email" = "Email";
"password" = "Kata Sandi";
"confirm_password" = "Konfirmasi Kata Sandi";
"name" = "Nama Lengkap";
"forgot_password" = "Lupa Kata Sandi?";
"dont_have_account" = "Belum punya akun? Daftar";
"already_have_account" = "Sudah punya akun? Masuk";
"send_reset_link" = "Kirim Link Reset";
"reset_link_sent" = "Cek email kamu untuk link reset kata sandi.";

/* Validation */
"invalid_email" = "Masukkan alamat email yang valid";
"password_too_short" = "Kata sandi minimal 8 karakter";
"passwords_dont_match" = "Kata sandi tidak cocok";
"name_required" = "Nama wajib diisi";

/* Tabs & Home */
"home" = "Beranda";
"explore" = "Jelajah";
"profile" = "Profil";
"no_items" = "Belum ada item";
"pull_to_refresh" = "Tarik untuk refresh atau ketuk coba lagi";

/* Settings */
"settings" = "Pengaturan";
"notifications" = "Notifikasi";
"theme" = "Tema";
"language" = "Bahasa";
"about" = "Tentang";
"version" = "Versi";
"terms_of_service" = "Syarat Layanan";
"privacy_policy" = "Kebijakan Privasi";
"logout" = "Keluar";
"dark" = "Gelap";
"light" = "Terang";
"system" = "Sistem";

/* States */
"something_went_wrong" = "Terjadi kesalahan";
"no_connection" = "Tidak ada koneksi internet";
"empty_here" = "Belum ada apa-apa di sini";
"coming_soon" = "Segera hadir";
```

- [ ] **Step 3: Create Strings.swift**

```swift
import Foundation

enum Strings {
    static let appName = String(localized: "app_name")
    static let ok = String(localized: "ok")
    static let cancel = String(localized: "cancel")
    static let error = String(localized: "error")
    static let retry = String(localized: "retry")
    static let loading = String(localized: "loading")

    static let onboardingTitle1 = String(localized: "onboarding_title_1")
    static let onboardingSubtitle1 = String(localized: "onboarding_subtitle_1")
    static let onboardingTitle2 = String(localized: "onboarding_title_2")
    static let onboardingSubtitle2 = String(localized: "onboarding_subtitle_2")
    static let onboardingTitle3 = String(localized: "onboarding_title_3")
    static let onboardingSubtitle3 = String(localized: "onboarding_subtitle_3")
    static let skip = String(localized: "skip")
    static let next = String(localized: "next")
    static let getStarted = String(localized: "get_started")

    static let login = String(localized: "login")
    static let register = String(localized: "register")
    static let email = String(localized: "email")
    static let password = String(localized: "password")
    static let confirmPassword = String(localized: "confirm_password")
    static let name = String(localized: "name")
    static let forgotPassword = String(localized: "forgot_password")
    static let dontHaveAccount = String(localized: "dont_have_account")
    static let alreadyHaveAccount = String(localized: "already_have_account")
    static let sendResetLink = String(localized: "send_reset_link")
    static let resetLinkSent = String(localized: "reset_link_sent")

    static let invalidEmail = String(localized: "invalid_email")
    static let passwordTooShort = String(localized: "password_too_short")
    static let passwordsDontMatch = String(localized: "passwords_dont_match")
    static let nameRequired = String(localized: "name_required")

    static let home = String(localized: "home")
    static let explore = String(localized: "explore")
    static let profile = String(localized: "profile")
    static let noItems = String(localized: "no_items")
    static let pullToRefresh = String(localized: "pull_to_refresh")

    static let settings = String(localized: "settings")
    static let notifications = String(localized: "notifications")
    static let theme = String(localized: "theme")
    static let language = String(localized: "language")
    static let about = String(localized: "about")
    static let version = String(localized: "version")
    static let termsOfService = String(localized: "terms_of_service")
    static let privacyPolicy = String(localized: "privacy_policy")
    static let logout = String(localized: "logout")
    static let dark = String(localized: "dark")
    static let light = String(localized: "light")
    static let system = String(localized: "system")

    static let somethingWentWrong = String(localized: "something_went_wrong")
    static let noConnection = String(localized: "no_connection")
    static let emptyHere = String(localized: "empty_here")
    static let comingSoon = String(localized: "coming_soon")
}
```

- [ ] **Step 4: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 5: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Core/Localization/ products/swiftui-starter-kit/SwiftUIStarterKit/Constants/Strings.swift
git commit -m "feat(swiftui-starter-kit): add localization (EN + ID) and strings constants"
```

---

### Task 7: SharedUI Components

**Files:**
- Create: `SwiftUIStarterKit/SharedUI/LoadingView.swift`
- Create: `SwiftUIStarterKit/SharedUI/EmptyStateView.swift`
- Create: `SwiftUIStarterKit/SharedUI/ErrorStateView.swift`
- Create: `SwiftUIStarterKit/SharedUI/PrimaryButton.swift`
- Create: `SwiftUIStarterKit/SharedUI/InputField.swift`
- Create: `SwiftUIStarterKit/SharedUI/AvatarView.swift`

- [ ] **Step 1: Create LoadingView.swift**

```swift
import SwiftUI

struct LoadingView: View {
    var message: String?

    var body: some View {
        VStack(spacing: AppTheme.spacingMD) {
            ProgressView()
                .controlSize(.large)
            if let message {
                Text(message)
                    .font(AppTheme.captionFont)
                    .foregroundStyle(AppColors.textSecondary)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
```

- [ ] **Step 2: Create EmptyStateView.swift**

```swift
import SwiftUI

struct EmptyStateView: View {
    let icon: String
    let title: String
    let subtitle: String
    var buttonTitle: String?
    var onAction: (() -> Void)?

    var body: some View {
        VStack(spacing: AppTheme.spacingMD) {
            Image(systemName: icon)
                .font(.system(size: 56))
                .foregroundStyle(AppColors.textSecondary)
            Text(title)
                .font(AppTheme.headlineFont)
                .foregroundStyle(AppColors.textPrimary)
            Text(subtitle)
                .font(AppTheme.bodyFont)
                .foregroundStyle(AppColors.textSecondary)
                .multilineTextAlignment(.center)
            if let buttonTitle, let onAction {
                PrimaryButton(title: buttonTitle, action: onAction)
                    .padding(.top, AppTheme.spacingSM)
            }
        }
        .padding(AppTheme.spacingXL)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
```

- [ ] **Step 3: Create ErrorStateView.swift**

```swift
import SwiftUI

struct ErrorStateView: View {
    let message: String
    var onRetry: (() -> Void)?

    var body: some View {
        VStack(spacing: AppTheme.spacingMD) {
            Image(systemName: "exclamationmark.triangle")
                .font(.system(size: 56))
                .foregroundStyle(AppColors.error)
            Text(Strings.error)
                .font(AppTheme.headlineFont)
                .foregroundStyle(AppColors.textPrimary)
            Text(message)
                .font(AppTheme.bodyFont)
                .foregroundStyle(AppColors.textSecondary)
                .multilineTextAlignment(.center)
            if let onRetry {
                PrimaryButton(title: Strings.retry, action: onRetry)
                    .padding(.top, AppTheme.spacingSM)
            }
        }
        .padding(AppTheme.spacingXL)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
```

- [ ] **Step 4: Create PrimaryButton.swift**

```swift
import SwiftUI

struct PrimaryButton: View {
    let title: String
    var isLoading: Bool = false
    var isDisabled: Bool = false
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Group {
                if isLoading {
                    ProgressView()
                        .tint(.white)
                } else {
                    Text(title)
                        .font(AppTheme.buttonFont)
                }
            }
            .frame(maxWidth: .infinity)
            .frame(height: 50)
            .background(isDisabled ? AppColors.textSecondary : AppColors.primary)
            .foregroundStyle(.white)
            .clipShape(RoundedRectangle(cornerRadius: AppTheme.cornerRadiusMD))
        }
        .disabled(isLoading || isDisabled)
    }
}
```

- [ ] **Step 5: Create InputField.swift**

```swift
import SwiftUI

struct InputField: View {
    let label: String
    @Binding var text: String
    var placeholder: String = ""
    var isSecure: Bool = false
    var error: String?
    var keyboardType: UIKeyboardType = .default

    @State private var showPassword = false

    var body: some View {
        VStack(alignment: .leading, spacing: AppTheme.spacingXS) {
            Text(label)
                .font(AppTheme.captionFont)
                .foregroundStyle(AppColors.textSecondary)

            HStack {
                if isSecure && !showPassword {
                    SecureField(placeholder, text: $text)
                } else {
                    TextField(placeholder, text: $text)
                        .keyboardType(keyboardType)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                }
                if isSecure {
                    Button { showPassword.toggle() } label: {
                        Image(systemName: showPassword ? "eye.slash" : "eye")
                            .foregroundStyle(AppColors.textSecondary)
                    }
                }
            }
            .font(AppTheme.bodyFont)
            .padding(12)
            .background(AppColors.surface)
            .clipShape(RoundedRectangle(cornerRadius: AppTheme.cornerRadiusSM))
            .overlay(
                RoundedRectangle(cornerRadius: AppTheme.cornerRadiusSM)
                    .stroke(error != nil ? AppColors.error : .clear, lineWidth: 1)
            )

            if let error {
                Text(error)
                    .font(AppTheme.captionFont)
                    .foregroundStyle(AppColors.error)
            }
        }
    }
}
```

- [ ] **Step 6: Create AvatarView.swift**

```swift
import SwiftUI

struct AvatarView: View {
    let name: String
    var size: CGFloat = 48
    var imageURL: URL?

    private var initials: String {
        let parts = name.split(separator: " ")
        let first = parts.first?.prefix(1) ?? ""
        let last = parts.count > 1 ? parts.last!.prefix(1) : ""
        return "\(first)\(last)".uppercased()
    }

    var body: some View {
        if let imageURL {
            AsyncImage(url: imageURL) { image in
                image.resizable().scaledToFill()
            } placeholder: {
                initialsView
            }
            .frame(width: size, height: size)
            .clipShape(Circle())
        } else {
            initialsView
        }
    }

    private var initialsView: some View {
        ZStack {
            Circle().fill(AppColors.primary.opacity(0.2))
            Text(initials)
                .font(.system(size: size * 0.4, weight: .semibold))
                .foregroundStyle(AppColors.primary)
        }
        .frame(width: size, height: size)
    }
}
```

- [ ] **Step 7: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 8: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/SharedUI/
git commit -m "feat(swiftui-starter-kit): add shared UI components"
```

---

### Task 8: Onboarding Module

**Files:**
- Create: `SwiftUIStarterKit/Modules/Onboarding/OnboardingEntity.swift`
- Create: `SwiftUIStarterKit/Modules/Onboarding/OnboardingInteractor.swift`
- Create: `SwiftUIStarterKit/Modules/Onboarding/OnboardingPresenter.swift`
- Create: `SwiftUIStarterKit/Modules/Onboarding/OnboardingView.swift`
- Create: `SwiftUIStarterKit/Modules/Onboarding/OnboardingRouter.swift`

- [ ] **Step 1: Create OnboardingEntity.swift**

```swift
import Foundation

struct OnboardingPage: Identifiable {
    let id = UUID()
    let image: String
    let title: String
    let subtitle: String
}
```

- [ ] **Step 2: Create OnboardingInteractor.swift**

```swift
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
```

- [ ] **Step 3: Create OnboardingPresenter.swift**

```swift
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
```

- [ ] **Step 4: Create OnboardingView.swift**

```swift
import SwiftUI

struct OnboardingView: View {
    @ObservedObject var presenter: OnboardingPresenter

    var body: some View {
        VStack {
            HStack {
                Spacer()
                if !presenter.isLastPage {
                    Button(Strings.skip) { presenter.skip() }
                        .font(AppTheme.bodyFont)
                        .foregroundStyle(AppColors.textSecondary)
                }
            }
            .padding(.horizontal, AppTheme.spacingMD)
            .frame(height: 44)

            TabView(selection: $presenter.currentPage) {
                ForEach(Array(presenter.pages.enumerated()), id: \.element.id) { index, page in
                    VStack(spacing: AppTheme.spacingLG) {
                        Spacer()
                        Image(systemName: page.image)
                            .font(.system(size: 80))
                            .foregroundStyle(AppColors.primary)
                        Text(page.title)
                            .font(AppTheme.titleFont)
                            .foregroundStyle(AppColors.textPrimary)
                        Text(page.subtitle)
                            .font(AppTheme.bodyFont)
                            .foregroundStyle(AppColors.textSecondary)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal, AppTheme.spacingXL)
                        Spacer()
                    }
                    .tag(index)
                }
            }
            .tabViewStyle(.page(indexDisplayMode: .always))

            PrimaryButton(
                title: presenter.isLastPage ? Strings.getStarted : Strings.next
            ) {
                withAnimation { presenter.nextPage() }
            }
            .padding(.horizontal, AppTheme.spacingMD)
            .padding(.bottom, AppTheme.spacingXL)
        }
        .background(AppColors.background)
    }
}
```

- [ ] **Step 5: Create OnboardingRouter.swift**

```swift
import SwiftUI

enum OnboardingRouter {
    static func createModule(onComplete: @escaping () -> Void) -> some View {
        let interactor = OnboardingInteractor()
        let presenter = OnboardingPresenter(interactor: interactor, onComplete: onComplete)
        return OnboardingView(presenter: presenter)
    }
}
```

- [ ] **Step 6: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 7: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Modules/Onboarding/
git commit -m "feat(swiftui-starter-kit): add onboarding module (VIPER)"
```

---

### Task 9: Auth Module

**Files:**
- Create: `SwiftUIStarterKit/Modules/Auth/AuthEntity.swift`
- Create: `SwiftUIStarterKit/Modules/Auth/AuthInteractor.swift`
- Create: `SwiftUIStarterKit/Modules/Auth/AuthPresenter.swift`
- Create: `SwiftUIStarterKit/Modules/Auth/LoginView.swift`
- Create: `SwiftUIStarterKit/Modules/Auth/RegisterView.swift`
- Create: `SwiftUIStarterKit/Modules/Auth/ForgotPasswordView.swift`
- Create: `SwiftUIStarterKit/Modules/Auth/AuthRouter.swift`

- [ ] **Step 1: Create AuthEntity.swift**

```swift
import Foundation

struct AuthResponse: Codable {
    let token: String
    let user: User
}

struct User: Codable, Identifiable {
    let id: String
    let name: String
    let email: String
}

struct ForgotPasswordResponse: Codable {
    let message: String
}

enum AuthEndpoint: APIEndpoint {
    case login(email: String, password: String)
    case register(name: String, email: String, password: String)
    case forgotPassword(email: String)

    var path: String {
        switch self {
        case .login: "/auth/login"
        case .register: "/auth/register"
        case .forgotPassword: "/auth/forgot-password"
        }
    }

    var method: HTTPMethod { .post }

    var body: Data? {
        switch self {
        case .login(let email, let password):
            try? JSONEncoder().encode(["email": email, "password": password])
        case .register(let name, let email, let password):
            try? JSONEncoder().encode(["name": name, "email": email, "password": password])
        case .forgotPassword(let email):
            try? JSONEncoder().encode(["email": email])
        }
    }
}
```

- [ ] **Step 2: Create AuthInteractor.swift**

```swift
import Foundation

protocol AuthInteractorProtocol {
    func login(email: String, password: String) async throws -> AuthResponse
    func register(name: String, email: String, password: String) async throws -> AuthResponse
    func forgotPassword(email: String) async throws
}

class AuthInteractor: AuthInteractorProtocol {
    private let apiClient: APIClientProtocol

    init(apiClient: APIClientProtocol = MockAPIClient.shared) {
        self.apiClient = apiClient
    }

    func login(email: String, password: String) async throws -> AuthResponse {
        let response: AuthResponse = try await apiClient.request(
            AuthEndpoint.login(email: email, password: password)
        )
        KeychainManager.shared.saveToken(response.token)
        return response
    }

    func register(name: String, email: String, password: String) async throws -> AuthResponse {
        let response: AuthResponse = try await apiClient.request(
            AuthEndpoint.register(name: name, email: email, password: password)
        )
        KeychainManager.shared.saveToken(response.token)
        return response
    }

    func forgotPassword(email: String) async throws {
        let _: ForgotPasswordResponse = try await apiClient.request(
            AuthEndpoint.forgotPassword(email: email)
        )
    }
}
```

- [ ] **Step 3: Create AuthPresenter.swift**

```swift
import Combine

class AuthPresenter: ObservableObject {
    @Published var loginEmail = ""
    @Published var loginPassword = ""
    @Published var registerName = ""
    @Published var registerEmail = ""
    @Published var registerPassword = ""
    @Published var registerConfirmPassword = ""
    @Published var forgotEmail = ""
    @Published var forgotSent = false
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let interactor: AuthInteractorProtocol
    private let onSuccess: () -> Void

    init(interactor: AuthInteractorProtocol, onSuccess: @escaping () -> Void) {
        self.interactor = interactor
        self.onSuccess = onSuccess
    }

    // MARK: - Validation

    var loginEmailError: String? {
        guard !loginEmail.isEmpty else { return nil }
        return loginEmail.isValidEmail ? nil : Strings.invalidEmail
    }

    var loginPasswordError: String? {
        guard !loginPassword.isEmpty else { return nil }
        return loginPassword.count >= AppConstants.minPasswordLength ? nil : Strings.passwordTooShort
    }

    var isLoginValid: Bool {
        loginEmail.isValidEmail && loginPassword.count >= AppConstants.minPasswordLength
    }

    var registerNameError: String? {
        guard !registerName.isEmpty else { return nil }
        return registerName.trimmed.isEmpty ? Strings.nameRequired : nil
    }

    var registerEmailError: String? {
        guard !registerEmail.isEmpty else { return nil }
        return registerEmail.isValidEmail ? nil : Strings.invalidEmail
    }

    var registerPasswordError: String? {
        guard !registerPassword.isEmpty else { return nil }
        return registerPassword.count >= AppConstants.minPasswordLength ? nil : Strings.passwordTooShort
    }

    var registerConfirmError: String? {
        guard !registerConfirmPassword.isEmpty else { return nil }
        return registerConfirmPassword == registerPassword ? nil : Strings.passwordsDontMatch
    }

    var isRegisterValid: Bool {
        !registerName.trimmed.isEmpty
        && registerEmail.isValidEmail
        && registerPassword.count >= AppConstants.minPasswordLength
        && registerConfirmPassword == registerPassword
    }

    var isForgotValid: Bool { forgotEmail.isValidEmail }

    // MARK: - Actions

    @MainActor
    func login() async {
        isLoading = true; errorMessage = nil
        do {
            _ = try await interactor.login(email: loginEmail, password: loginPassword)
            onSuccess()
        } catch { errorMessage = error.localizedDescription }
        isLoading = false
    }

    @MainActor
    func register() async {
        isLoading = true; errorMessage = nil
        do {
            _ = try await interactor.register(name: registerName, email: registerEmail, password: registerPassword)
            onSuccess()
        } catch { errorMessage = error.localizedDescription }
        isLoading = false
    }

    @MainActor
    func forgotPassword() async {
        isLoading = true; errorMessage = nil
        do {
            try await interactor.forgotPassword(email: forgotEmail)
            forgotSent = true
        } catch { errorMessage = error.localizedDescription }
        isLoading = false
    }
}
```

- [ ] **Step 4: Create LoginView.swift**

```swift
import SwiftUI

struct LoginView: View {
    @ObservedObject var presenter: AuthPresenter

    var body: some View {
        ScrollView {
            VStack(spacing: AppTheme.spacingMD) {
                Spacer().frame(height: AppTheme.spacingXL)

                Text(Strings.login)
                    .font(AppTheme.titleFont)
                    .foregroundStyle(AppColors.textPrimary)

                InputField(
                    label: Strings.email, text: $presenter.loginEmail,
                    placeholder: "john@example.com",
                    error: presenter.loginEmailError, keyboardType: .emailAddress
                )
                InputField(
                    label: Strings.password, text: $presenter.loginPassword,
                    placeholder: "********", isSecure: true,
                    error: presenter.loginPasswordError
                )

                NavigationLink {
                    ForgotPasswordView(presenter: presenter)
                } label: {
                    Text(Strings.forgotPassword)
                        .font(AppTheme.captionFont)
                        .foregroundStyle(AppColors.primary)
                        .frame(maxWidth: .infinity, alignment: .trailing)
                }

                if let error = presenter.errorMessage {
                    Text(error).font(AppTheme.captionFont).foregroundStyle(AppColors.error)
                }

                PrimaryButton(
                    title: Strings.login,
                    isLoading: presenter.isLoading,
                    isDisabled: !presenter.isLoginValid
                ) { Task { await presenter.login() } }

                NavigationLink {
                    RegisterView(presenter: presenter)
                } label: {
                    Text(Strings.dontHaveAccount)
                        .font(AppTheme.bodyFont)
                        .foregroundStyle(AppColors.textSecondary)
                }
                .padding(.top, AppTheme.spacingSM)
            }
            .padding(.horizontal, AppTheme.spacingMD)
        }
        .background(AppColors.background)
        .onTapGesture { hideKeyboard() }
    }
}
```

- [ ] **Step 5: Create RegisterView.swift**

```swift
import SwiftUI

struct RegisterView: View {
    @ObservedObject var presenter: AuthPresenter

    var body: some View {
        ScrollView {
            VStack(spacing: AppTheme.spacingMD) {
                Spacer().frame(height: AppTheme.spacingLG)

                Text(Strings.register)
                    .font(AppTheme.titleFont)
                    .foregroundStyle(AppColors.textPrimary)

                InputField(label: Strings.name, text: $presenter.registerName, placeholder: "John Doe", error: presenter.registerNameError)
                InputField(label: Strings.email, text: $presenter.registerEmail, placeholder: "john@example.com", error: presenter.registerEmailError, keyboardType: .emailAddress)
                InputField(label: Strings.password, text: $presenter.registerPassword, placeholder: "********", isSecure: true, error: presenter.registerPasswordError)
                InputField(label: Strings.confirmPassword, text: $presenter.registerConfirmPassword, placeholder: "********", isSecure: true, error: presenter.registerConfirmError)

                if let error = presenter.errorMessage {
                    Text(error).font(AppTheme.captionFont).foregroundStyle(AppColors.error)
                }

                PrimaryButton(
                    title: Strings.register,
                    isLoading: presenter.isLoading,
                    isDisabled: !presenter.isRegisterValid
                ) { Task { await presenter.register() } }

                NavigationLink {
                    LoginView(presenter: presenter)
                } label: {
                    Text(Strings.alreadyHaveAccount)
                        .font(AppTheme.bodyFont)
                        .foregroundStyle(AppColors.textSecondary)
                }
                .padding(.top, AppTheme.spacingSM)
            }
            .padding(.horizontal, AppTheme.spacingMD)
        }
        .background(AppColors.background)
        .onTapGesture { hideKeyboard() }
        .navigationBarTitleDisplayMode(.inline)
    }
}
```

- [ ] **Step 6: Create ForgotPasswordView.swift**

```swift
import SwiftUI

struct ForgotPasswordView: View {
    @ObservedObject var presenter: AuthPresenter

    var body: some View {
        VStack(spacing: AppTheme.spacingMD) {
            Spacer()

            if presenter.forgotSent {
                Image(systemName: "envelope.badge.fill")
                    .font(.system(size: 56))
                    .foregroundStyle(AppColors.primary)
                Text(Strings.resetLinkSent)
                    .font(AppTheme.headlineFont)
                    .foregroundStyle(AppColors.textPrimary)
                    .multilineTextAlignment(.center)
            } else {
                Text(Strings.forgotPassword)
                    .font(AppTheme.titleFont)
                    .foregroundStyle(AppColors.textPrimary)

                InputField(label: Strings.email, text: $presenter.forgotEmail, placeholder: "john@example.com", keyboardType: .emailAddress)

                if let error = presenter.errorMessage {
                    Text(error).font(AppTheme.captionFont).foregroundStyle(AppColors.error)
                }

                PrimaryButton(
                    title: Strings.sendResetLink,
                    isLoading: presenter.isLoading,
                    isDisabled: !presenter.isForgotValid
                ) { Task { await presenter.forgotPassword() } }
            }

            Spacer()
        }
        .padding(.horizontal, AppTheme.spacingMD)
        .background(AppColors.background)
        .onTapGesture { hideKeyboard() }
        .navigationBarTitleDisplayMode(.inline)
    }
}
```

- [ ] **Step 7: Create AuthRouter.swift**

```swift
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
```

- [ ] **Step 8: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 9: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Modules/Auth/
git commit -m "feat(swiftui-starter-kit): add auth module (login, register, forgot password)"
```

---

### Task 10: Home Module

**Files:**
- Create: `SwiftUIStarterKit/Modules/Home/HomeEntity.swift`
- Create: `SwiftUIStarterKit/Modules/Home/HomeInteractor.swift`
- Create: `SwiftUIStarterKit/Modules/Home/HomePresenter.swift`
- Create: `SwiftUIStarterKit/Modules/Home/HomeView.swift`
- Create: `SwiftUIStarterKit/Modules/Home/HomeRouter.swift`

- [ ] **Step 1: Create HomeEntity.swift**

```swift
import Foundation

struct HomeItem: Codable, Identifiable {
    let id: String
    let title: String
    let subtitle: String
}

enum HomeEndpoint: APIEndpoint {
    case fetchItems

    var path: String { "/items" }
    var method: HTTPMethod { .get }
}
```

- [ ] **Step 2: Create HomeInteractor.swift**

```swift
import Foundation

protocol HomeInteractorProtocol {
    func fetchItems() async throws -> [HomeItem]
}

class HomeInteractor: HomeInteractorProtocol {
    private let apiClient: APIClientProtocol

    init(apiClient: APIClientProtocol = MockAPIClient.shared) {
        self.apiClient = apiClient
    }

    func fetchItems() async throws -> [HomeItem] {
        try await apiClient.request(HomeEndpoint.fetchItems)
    }
}
```

- [ ] **Step 3: Create HomePresenter.swift**

```swift
import Combine

enum HomeState {
    case loading, loaded([HomeItem]), empty, error(String)
}

class HomePresenter: ObservableObject {
    @Published var state: HomeState = .loading

    private let interactor: HomeInteractorProtocol

    init(interactor: HomeInteractorProtocol) {
        self.interactor = interactor
    }

    @MainActor
    func fetchItems() async {
        state = .loading
        do {
            let items = try await interactor.fetchItems()
            state = items.isEmpty ? .empty : .loaded(items)
        } catch {
            state = .error(error.localizedDescription)
        }
    }
}
```

- [ ] **Step 4: Create HomeView.swift**

```swift
import SwiftUI

struct HomeView: View {
    @ObservedObject var presenter: HomePresenter

    var body: some View {
        NavigationStack {
            Group {
                switch presenter.state {
                case .loading:
                    LoadingView(message: Strings.loading)
                case .loaded(let items):
                    List(items) { item in
                        VStack(alignment: .leading, spacing: AppTheme.spacingXS) {
                            Text(item.title)
                                .font(AppTheme.headlineFont)
                                .foregroundStyle(AppColors.textPrimary)
                            Text(item.subtitle)
                                .font(AppTheme.bodyFont)
                                .foregroundStyle(AppColors.textSecondary)
                        }
                        .padding(.vertical, AppTheme.spacingXS)
                    }
                    .refreshable { await presenter.fetchItems() }
                case .empty:
                    EmptyStateView(
                        icon: "tray", title: Strings.emptyHere,
                        subtitle: Strings.pullToRefresh, buttonTitle: Strings.retry
                    ) { Task { await presenter.fetchItems() } }
                case .error(let message):
                    ErrorStateView(message: message) {
                        Task { await presenter.fetchItems() }
                    }
                }
            }
            .navigationTitle(Strings.home)
        }
        .task { await presenter.fetchItems() }
    }
}
```

- [ ] **Step 5: Create HomeRouter.swift**

```swift
import SwiftUI

enum HomeRouter {
    static func createModule() -> some View {
        let interactor = HomeInteractor()
        let presenter = HomePresenter(interactor: interactor)
        return HomeView(presenter: presenter)
    }
}
```

- [ ] **Step 6: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 7: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Modules/Home/
git commit -m "feat(swiftui-starter-kit): add home module with pull-to-refresh"
```

---

### Task 11: Settings Module

**Files:**
- Create: `SwiftUIStarterKit/Modules/Settings/SettingsEntity.swift`
- Create: `SwiftUIStarterKit/Modules/Settings/SettingsInteractor.swift`
- Create: `SwiftUIStarterKit/Modules/Settings/SettingsPresenter.swift`
- Create: `SwiftUIStarterKit/Modules/Settings/SettingsView.swift`
- Create: `SwiftUIStarterKit/Modules/Settings/SettingsRouter.swift`

- [ ] **Step 1: Create SettingsEntity.swift**

```swift
import Foundation

struct UserProfile {
    let name: String
    let email: String
    let avatarURL: URL?
}
```

- [ ] **Step 2: Create SettingsInteractor.swift**

```swift
import Foundation

protocol SettingsInteractorProtocol {
    func getUserProfile() -> UserProfile
    func logout()
}

class SettingsInteractor: SettingsInteractorProtocol {
    private let onLogout: () -> Void

    init(onLogout: @escaping () -> Void) {
        self.onLogout = onLogout
    }

    func getUserProfile() -> UserProfile {
        UserProfile(name: "John Doe", email: "john@example.com", avatarURL: nil)
    }

    func logout() {
        KeychainManager.shared.deleteToken()
        onLogout()
    }
}
```

- [ ] **Step 3: Create SettingsPresenter.swift**

```swift
import Combine

class SettingsPresenter: ObservableObject {
    @Published var profile: UserProfile
    @Published var notificationsEnabled: Bool

    private let interactor: SettingsInteractorProtocol

    init(interactor: SettingsInteractorProtocol) {
        self.interactor = interactor
        self.profile = interactor.getUserProfile()
        self.notificationsEnabled = UserDefaultsManager.shared.notificationsEnabled
    }

    func toggleNotifications(_ value: Bool) {
        notificationsEnabled = value
        UserDefaultsManager.shared.notificationsEnabled = value
    }

    func logout() { interactor.logout() }

    var appVersion: String {
        Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0"
    }
}
```

- [ ] **Step 4: Create SettingsView.swift**

```swift
import SwiftUI

struct SettingsView: View {
    @ObservedObject var presenter: SettingsPresenter
    @EnvironmentObject var themeManager: ThemeManager

    var body: some View {
        NavigationStack {
            List {
                Section {
                    HStack(spacing: AppTheme.spacingMD) {
                        AvatarView(name: presenter.profile.name, size: 56, imageURL: presenter.profile.avatarURL)
                        VStack(alignment: .leading) {
                            Text(presenter.profile.name).font(AppTheme.headlineFont)
                            Text(presenter.profile.email)
                                .font(AppTheme.captionFont)
                                .foregroundStyle(AppColors.textSecondary)
                        }
                    }
                    .padding(.vertical, AppTheme.spacingXS)
                }

                Section(Strings.settings) {
                    Toggle(Strings.notifications, isOn: Binding(
                        get: { presenter.notificationsEnabled },
                        set: { presenter.toggleNotifications($0) }
                    ))

                    Picker(Strings.theme, selection: Binding(
                        get: { themeManager.currentTheme },
                        set: { themeManager.currentTheme = $0 }
                    )) {
                        ForEach(ThemeMode.allCases, id: \.self) { mode in
                            Text(mode.displayName).tag(mode)
                        }
                    }
                }

                Section(Strings.about) {
                    HStack {
                        Text(Strings.version)
                        Spacer()
                        Text(presenter.appVersion).foregroundStyle(AppColors.textSecondary)
                    }
                    Link(Strings.termsOfService, destination: URL(string: "https://example.com/terms")!)
                    Link(Strings.privacyPolicy, destination: URL(string: "https://example.com/privacy")!)
                }

                Section {
                    Button(role: .destructive) { presenter.logout() } label: {
                        HStack { Spacer(); Text(Strings.logout); Spacer() }
                    }
                }
            }
            .navigationTitle(Strings.settings)
        }
    }
}
```

- [ ] **Step 5: Create SettingsRouter.swift**

```swift
import SwiftUI

enum SettingsRouter {
    static func createModule(onLogout: @escaping () -> Void) -> some View {
        let interactor = SettingsInteractor(onLogout: onLogout)
        let presenter = SettingsPresenter(interactor: interactor)
        return SettingsView(presenter: presenter)
    }
}
```

- [ ] **Step 6: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 7: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Modules/Settings/
git commit -m "feat(swiftui-starter-kit): add settings module with theme picker"
```

---

### Task 12: TabBar Module

**Files:**
- Create: `SwiftUIStarterKit/Modules/TabBar/TabBarEntity.swift`
- Create: `SwiftUIStarterKit/Modules/TabBar/TabBarView.swift`
- Create: `SwiftUIStarterKit/Modules/TabBar/TabBarRouter.swift`

- [ ] **Step 1: Create TabBarEntity.swift**

```swift
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
```

- [ ] **Step 2: Create TabBarView.swift**

```swift
import SwiftUI

struct TabBarView: View {
    @State private var selectedTab: TabItem = .home
    let onLogout: () -> Void

    var body: some View {
        TabView(selection: $selectedTab) {
            ForEach(TabItem.allCases) { tab in
                tabContent(for: tab)
                    .tabItem {
                        Image(systemName: tab.icon)
                        Text(tab.title)
                    }
                    .tag(tab)
            }
        }
        .tint(AppColors.primary)
    }

    @ViewBuilder
    private func tabContent(for tab: TabItem) -> some View {
        switch tab {
        case .home:
            HomeRouter.createModule()
        case .explore:
            placeholderTab(title: Strings.explore, icon: "magnifyingglass")
        case .profile:
            placeholderTab(title: Strings.profile, icon: "person.fill")
        case .settings:
            SettingsRouter.createModule(onLogout: onLogout)
        }
    }

    private func placeholderTab(title: String, icon: String) -> some View {
        NavigationStack {
            EmptyStateView(icon: icon, title: title, subtitle: Strings.comingSoon)
                .navigationTitle(title)
        }
    }
}
```

- [ ] **Step 3: Create TabBarRouter.swift**

```swift
import SwiftUI

enum TabBarRouter {
    static func createModule(onLogout: @escaping () -> Void) -> some View {
        TabBarView(onLogout: onLogout)
    }
}
```

- [ ] **Step 4: Regenerate + verify build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

- [ ] **Step 5: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/Modules/TabBar/
git commit -m "feat(swiftui-starter-kit): add tab bar module (4 tabs)"
```

---

### Task 13: App Entry + AppRouter + Push Notifications

**Files:**
- Create: `SwiftUIStarterKit/App/AppRouter.swift`
- Create: `SwiftUIStarterKit/App/AppDelegate.swift`
- Create: `SwiftUIStarterKit/Core/Notifications/NotificationManager.swift`
- Modify: `SwiftUIStarterKit/App/SwiftUIStarterKitApp.swift`

- [ ] **Step 1: Create AppRouter.swift**

```swift
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
```

- [ ] **Step 2: Create AppDelegate.swift**

```swift
import UIKit
import UserNotifications

class AppDelegate: NSObject, UIApplicationDelegate, UNUserNotificationCenterDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        UNUserNotificationCenter.current().delegate = self
        return true
    }

    func application(
        _ application: UIApplication,
        didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
    ) {
        let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
        NotificationManager.shared.deviceToken = token
    }

    func application(
        _ application: UIApplication,
        didFailToRegisterForRemoteNotificationsWithError error: Error
    ) {
        print("Push registration failed: \(error.localizedDescription)")
    }

    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        [.banner, .badge, .sound]
    }
}
```

- [ ] **Step 3: Create NotificationManager.swift**

```swift
import Foundation
import UserNotifications
import UIKit

class NotificationManager: ObservableObject {
    static let shared = NotificationManager()
    @Published var isAuthorized = false
    var deviceToken: String?
    private init() {}

    func requestPermission() async {
        do {
            let granted = try await UNUserNotificationCenter.current()
                .requestAuthorization(options: [.alert, .badge, .sound])
            await MainActor.run {
                isAuthorized = granted
                if granted { UIApplication.shared.registerForRemoteNotifications() }
            }
        } catch {
            print("Notification permission error: \(error.localizedDescription)")
        }
    }
}
```

- [ ] **Step 4: Update SwiftUIStarterKitApp.swift (replace placeholder)**

```swift
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
```

- [ ] **Step 5: Regenerate + verify FULL build**

```bash
cd products/swiftui-starter-kit && xcodegen generate
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit -sdk iphonesimulator -quiet build
```

Expected: BUILD SUCCEEDED — full app compiles with all modules wired together.

- [ ] **Step 6: Commit**

```bash
git add products/swiftui-starter-kit/SwiftUIStarterKit/App/ products/swiftui-starter-kit/SwiftUIStarterKit/Core/Notifications/
git commit -m "feat(swiftui-starter-kit): wire app entry, routing, and push notifications"
```

---

### Task 14: Build Fix + Smoke Test

If the build in Task 13 failed, fix compile errors here. If it succeeded, run on simulator to verify the UI works.

- [ ] **Step 1: Run on iPhone simulator**

```bash
cd products/swiftui-starter-kit
xcrun simctl boot "iPhone 16" 2>/dev/null || true
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit \
  -destination 'platform=iOS Simulator,name=iPhone 16' -quiet build
```

- [ ] **Step 2: Run on iPad simulator**

```bash
xcodebuild -project SwiftUIStarterKit.xcodeproj -scheme SwiftUIStarterKit \
  -destination 'platform=iOS Simulator,name=iPad Pro 13-inch (M4)' -quiet build
```

- [ ] **Step 3: Fix any compilation errors**

If errors, fix the relevant file and rebuild. Common issues:
- Missing imports: add `import SwiftUI` or `import Combine`
- Type mismatches: check protocol conformances match
- Ambiguous color names: ensure Asset Catalog names match `AppColors` references

- [ ] **Step 4: Commit fixes if any**

```bash
git add -u products/swiftui-starter-kit/
git commit -m "fix(swiftui-starter-kit): resolve build issues"
```

---

### Task 15: Documentation

**Files:**
- Create: `products/swiftui-starter-kit/README.md`
- Create: `products/swiftui-starter-kit/CUSTOMIZATION.md`
- Create: `products/swiftui-starter-kit/ARCHITECTURE.md`
- Create: `products/swiftui-starter-kit/LICENSE`

- [ ] **Step 1: Create README.md**

```markdown
# SwiftUI Starter Kit

A production-ready iOS & iPad app boilerplate built with **VIPER architecture** and **SwiftUI**. Open, build, run — and start building your app on top of a clean, scalable foundation.

## Quick Start

1. Open `SwiftUIStarterKit.xcodeproj` in Xcode 16+
2. Select a simulator (iPhone or iPad)
3. Press **Cmd + R** to build and run

That's it. The app runs with mock data out of the box.

## Features

- [x] **Onboarding** — 3 swipeable pages with skip/next
- [x] **Authentication** — Login, Register, Forgot Password (custom, no vendor lock-in)
- [x] **Tab Navigation** — 4 tabs with SF Symbols
- [x] **Home Feed** — List with pull-to-refresh, loading/empty/error states
- [x] **Settings** — Profile, theme picker, notifications toggle, about section, logout
- [x] **Dark Mode** — System/Light/Dark toggle, applies instantly
- [x] **Networking** — Generic async/await API client with mock backend
- [x] **Keychain Storage** — Secure token storage (no third-party)
- [x] **Localization** — English + Bahasa Indonesia included
- [x] **Push Notifications** — Permission request + token handling ready

## Requirements

- Xcode 16+
- iOS 17+ / iPadOS 17+
- Swift 5.9+
- **Zero third-party dependencies**

## Architecture

VIPER pattern adapted for SwiftUI:

| Layer | Role | File |
|-------|------|------|
| **Router** | Creates module, wires dependencies | `*Router.swift` |
| **Interactor** | Business logic, API calls | `*Interactor.swift` |
| **Presenter** | ObservableObject, transforms data | `*Presenter.swift` |
| **View** | SwiftUI view, observes Presenter | `*View.swift` |
| **Entity** | Data models (Codable) | `*Entity.swift` |

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## Customization

See [CUSTOMIZATION.md](CUSTOMIZATION.md) for step-by-step guides:
- Rename the app
- Change theme colors
- Connect your real API
- Add a new VIPER module
- Add a new language
- Remove modules you don't need

## License

MIT License — use for personal and commercial projects.
```

- [ ] **Step 2: Create CUSTOMIZATION.md**

```markdown
# Customization Guide

## Rename the App

1. In Xcode: click project name in navigator → rename
2. Update `MARKETING_VERSION` in Build Settings
3. Update `bundleIdPrefix` in `project.yml` (if using XcodeGen)

## Change Theme Colors

Edit **one file**: `SwiftUIStarterKit/Core/Theme/AppTheme.swift` for fonts/spacing, or edit color assets in `Resources/Assets.xcassets/Colors/` for colors.

Each color has light and dark mode variants in the `.colorset/Contents.json` file.

## Connect Your Real API

1. Open `SwiftUIStarterKit/Constants/AppConstants.swift`
2. Change `apiBaseURL` to your server URL
3. In each module's Interactor `init()`, change `MockAPIClient.shared` to `APIClient.shared`

Example:
```swift
// Before (mock)
init(apiClient: APIClientProtocol = MockAPIClient.shared)

// After (real)
init(apiClient: APIClientProtocol = APIClient.shared)
```

## Add a New VIPER Module

1. Create folder: `Modules/YourModule/`
2. Create 5 files following the pattern:

- `YourModuleEntity.swift` — data models
- `YourModuleInteractor.swift` — protocol + class
- `YourModulePresenter.swift` — ObservableObject
- `YourModuleView.swift` — SwiftUI view
- `YourModuleRouter.swift` — static `createModule()`

3. Wire it in `TabBarView.swift` or navigate from another module

## Add a New Language

1. Create `Core/Localization/xx.lproj/Localizable.strings` (where `xx` = language code)
2. Copy all keys from `en.lproj/Localizable.strings`
3. Translate the values
4. If using XcodeGen, regenerate the project

## Remove a Module

1. Delete the module folder from `Modules/`
2. Remove references in `TabBarView.swift` or `AppRouter.swift`
3. Clean build (Cmd + Shift + K)
```

- [ ] **Step 3: Create ARCHITECTURE.md**

```markdown
# Architecture Guide

## VIPER Pattern

```
Router ──creates──▶ View
  │                    │
  │                    │ observes (@ObservedObject)
  │                    ▼
  │               Presenter (ObservableObject)
  │                    │
  │                    │ calls
  │                    ▼
  └──wires──▶   Interactor
                       │
                       │ uses
                       ▼
                    Entity (data models)
```

### Rules

- **1 type per file** — no multiple classes/structs in one file
- **Max 200 lines per file** — split when exceeding
- **No magic strings** — use `Constants/` and `StorageKeys`
- **No hardcoded colors** — use `AppColors` (from Asset Catalog)

### Layer Responsibilities

**Router** (`enum` with static methods)
- Creates Interactor → Presenter → View
- Returns `some View`
- No state, no stored properties

**Interactor** (`protocol` + `class`)
- Business logic and API calls
- Takes `APIClientProtocol` for testability
- Returns domain models, throws `APIError`

**Presenter** (`ObservableObject`)
- Holds `@Published` state
- Transforms Interactor output for View
- Handles input validation
- Uses `@MainActor` on async methods

**View** (SwiftUI `struct`)
- Pure display layer
- Observes Presenter via `@ObservedObject`
- No business logic

**Entity** (`struct: Codable`)
- Data models
- API endpoints (as conforming enums)

### File Naming

| File | Pattern |
|------|---------|
| Entity | `{Module}Entity.swift` |
| Interactor | `{Module}Interactor.swift` |
| Presenter | `{Module}Presenter.swift` |
| View | `{Module}View.swift` or `{Screen}View.swift` |
| Router | `{Module}Router.swift` |

### Navigation Flow

```
App Start
  │
  ├─ First launch ──▶ Onboarding ──▶ Auth
  ├─ Has token ──▶ TabBar (Main)
  └─ No token ──▶ Auth ──▶ TabBar (Main)

TabBar
  ├─ Home (list + pull-to-refresh)
  ├─ Explore (placeholder)
  ├─ Profile (placeholder)
  └─ Settings (theme, logout) ──▶ Auth
```

### Core Services

| Service | Singleton | Purpose |
|---------|-----------|---------|
| `APIClient` | `.shared` | HTTP requests |
| `MockAPIClient` | `.shared` | Preview/testing |
| `KeychainManager` | `.shared` | Secure token storage |
| `UserDefaultsManager` | `.shared` | App preferences |
| `ThemeManager` | `@EnvironmentObject` | Dark/light mode |
| `NotificationManager` | `.shared` | Push permission |
```

- [ ] **Step 4: Create LICENSE**

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 5: Commit**

```bash
git add products/swiftui-starter-kit/README.md products/swiftui-starter-kit/CUSTOMIZATION.md products/swiftui-starter-kit/ARCHITECTURE.md products/swiftui-starter-kit/LICENSE
git commit -m "docs(swiftui-starter-kit): add README, CUSTOMIZATION, ARCHITECTURE, LICENSE"
```

---

### Task 16: ZIP Packaging + Gumroad Listing

**Files:**
- Create: `products/swiftui-starter-kit/gumroad-listing.md`
- Create: `products/swiftui-starter-kit-v1.0.zip`

- [ ] **Step 1: Create gumroad-listing.md**

```markdown
# Gumroad Listing — SwiftUI Starter Kit

**Title:** SwiftUI Starter Kit — VIPER Boilerplate for iOS & iPad

**Price:** $29

**Tags:** SwiftUI, iOS, iPad, boilerplate, template, VIPER, starter kit, Xcode, Swift

**Thumbnail/Cover:** Screenshot collage (onboarding, login, home, settings, dark mode)

---

**Description:**

# SwiftUI Starter Kit — VIPER Boilerplate for iOS & iPad

Stop wasting time on app setup. Open → Build → Run → Start building.

## What You Get

A complete, production-ready SwiftUI Xcode project with:

**10 Features Ready Out of the Box:**
- Onboarding (3 swipeable pages)
- Authentication (Login, Register, Forgot Password)
- Tab Navigation (4 tabs with SF Symbols)
- Home Feed (list, pull-to-refresh)
- Settings (profile, theme, notifications, about, logout)
- Dark Mode (system/light/dark toggle)
- Networking (async/await API client + mock backend)
- Keychain Storage (secure tokens, no third-party)
- Localization (English + Indonesian)
- Push Notifications (permission + token handling)

**Architecture:**
- VIPER pattern — scalable, testable, clean separation
- 1 type per file, max 200 lines per file
- Zero third-party dependencies — pure Apple frameworks

**3 Detailed Docs:**
- README — quick start in 3 steps
- CUSTOMIZATION — rename app, change colors, connect API, add modules
- ARCHITECTURE — VIPER explanation, data flow, module communication

## Requirements
- Xcode 16+
- iOS 17+ / iPadOS 17+
- Swift 5.9+

## Who This Is For
- Indie iOS developers who want a head start
- Developers tired of repeating the same setup for every new app
- Anyone who wants clean, scalable architecture from day one

## License
MIT — use for personal and commercial projects. Build unlimited apps.
```

- [ ] **Step 2: Create ZIP (exclude dev files)**

```bash
cd products/swiftui-starter-kit
zip -r ../swiftui-starter-kit-v1.0.zip \
  SwiftUIStarterKit/ \
  SwiftUIStarterKit.xcodeproj/ \
  README.md \
  CUSTOMIZATION.md \
  ARCHITECTURE.md \
  LICENSE \
  -x "*.DS_Store" -x "__MACOSX/*"
```

- [ ] **Step 3: Verify ZIP contents**

```bash
unzip -l products/swiftui-starter-kit-v1.0.zip | head -60
```

- [ ] **Step 4: Commit ZIP + listing**

```bash
git add products/swiftui-starter-kit/gumroad-listing.md products/swiftui-starter-kit-v1.0.zip
git commit -m "feat(swiftui-starter-kit): add ZIP bundle and Gumroad listing"
```

---

## Summary

| Task | What | Files |
|------|------|-------|
| 1 | Project scaffold + xcodegen | 2 |
| 2 | Constants + Extensions | 5 |
| 3 | Theme + Color Assets | 3 + assets |
| 4 | Storage (Keychain + UserDefaults) | 2 |
| 5 | Network layer | 4 |
| 6 | Localization + Strings | 3 |
| 7 | SharedUI components | 6 |
| 8 | Onboarding module | 5 |
| 9 | Auth module | 7 |
| 10 | Home module | 5 |
| 11 | Settings module | 5 |
| 12 | TabBar module | 3 |
| 13 | App entry + routing + push | 4 |
| 14 | Build fix + smoke test | 0 |
| 15 | Documentation | 4 |
| 16 | ZIP packaging | 2 |

**Total: ~58 files, 16 tasks, ~16 commits**
