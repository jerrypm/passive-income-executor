# SwiftUI Starter Kit — VIPER Boilerplate for iOS & iPad

**Date:** 2026-04-11
**Product:** Gumroad digital product ($29)
**Target buyer:** Indie iOS developers who know Swift, want a head start
**Platform:** iOS 17+ / iPadOS 17+ (Universal)
**Architecture:** VIPER (Router → Interactor → Presenter → View → Entity)
**Dependencies:** Zero — pure Apple frameworks only
**Swift:** 5.9+, Xcode 16+

---

## Project Structure

```
SwiftUIStarterKit/
├── SwiftUIStarterKit.xcodeproj
├── SwiftUIStarterKit/
│   ├── App/
│   │   ├── SwiftUIStarterKitApp.swift      # @main entry, router setup
│   │   └── AppDelegate.swift                # Push notification registration
│   │
│   ├── Core/
│   │   ├── Network/
│   │   │   ├── APIClient.swift              # Generic async/await HTTP client
│   │   │   ├── APIEndpoint.swift            # Protocol + endpoint builder
│   │   │   ├── APIError.swift               # Typed errors
│   │   │   └── MockAPIClient.swift          # Preview/testing mock
│   │   ├── Storage/
│   │   │   ├── KeychainManager.swift        # Token/credential storage
│   │   │   ├── UserDefaultsManager.swift    # App preferences
│   │   │   └── StorageKeys.swift            # Centralized keys
│   │   ├── Theme/
│   │   │   ├── AppTheme.swift               # Colors, fonts, spacing
│   │   │   ├── ThemeManager.swift           # Dark/light/system toggle
│   │   │   └── AppColors.swift              # Color asset references
│   │   └── Localization/
│   │       ├── en.lproj/Localizable.strings
│   │       └── id.lproj/Localizable.strings
│   │
│   ├── Modules/
│   │   ├── Onboarding/
│   │   │   ├── OnboardingRouter.swift
│   │   │   ├── OnboardingInteractor.swift
│   │   │   ├── OnboardingPresenter.swift
│   │   │   ├── OnboardingView.swift         # Swipeable pages + skip/next
│   │   │   └── OnboardingEntity.swift
│   │   ├── Auth/
│   │   │   ├── AuthRouter.swift
│   │   │   ├── AuthInteractor.swift         # Login/register/forgot logic
│   │   │   ├── AuthPresenter.swift
│   │   │   ├── LoginView.swift
│   │   │   ├── RegisterView.swift
│   │   │   ├── ForgotPasswordView.swift
│   │   │   └── AuthEntity.swift             # User model, tokens
│   │   ├── Home/
│   │   │   ├── HomeRouter.swift
│   │   │   ├── HomeInteractor.swift
│   │   │   ├── HomePresenter.swift
│   │   │   ├── HomeView.swift
│   │   │   └── HomeEntity.swift
│   │   ├── Settings/
│   │   │   ├── SettingsRouter.swift
│   │   │   ├── SettingsInteractor.swift
│   │   │   ├── SettingsPresenter.swift
│   │   │   ├── SettingsView.swift           # Profile, notifications, theme, about
│   │   │   └── SettingsEntity.swift
│   │   └── TabBar/
│   │       ├── TabBarRouter.swift
│   │       ├── TabBarView.swift             # Bottom tabs (Home, Search, Profile, Settings)
│   │       └── TabBarEntity.swift
│   │
│   ├── SharedUI/
│   │   ├── LoadingView.swift
│   │   ├── EmptyStateView.swift
│   │   ├── ErrorStateView.swift
│   │   ├── PrimaryButton.swift
│   │   ├── InputField.swift
│   │   └── AvatarView.swift
│   │
│   ├── Extensions/
│   │   ├── View+Extensions.swift
│   │   ├── Color+Extensions.swift
│   │   └── String+Extensions.swift
│   │
│   ├── Constants/
│   │   ├── AppConstants.swift               # API base URL, app config
│   │   └── Strings.swift                    # All UI strings (localized)
│   │
│   └── Resources/
│       ├── Assets.xcassets                  # App icon, colors, images
│       └── Info.plist
│
├── README.md
├── CUSTOMIZATION.md
├── ARCHITECTURE.md
└── LICENSE
```

---

## Module Details

### Onboarding
- 3 swipeable pages via `TabView(.page)` with illustration placeholder, title, subtitle
- Skip button (top-right) + Next button + page indicator dots
- Last page: "Get Started" button navigates to Auth or TabBar
- `UserDefaults` flag `hasSeenOnboarding` — shows only on first launch
- iPad: adaptive layout with wider content area and larger illustrations

### Auth
- **LoginView:** email + password fields, "Forgot Password?" link, login button, "Don't have account? Register" link
- **RegisterView:** name + email + password + confirm password, register button
- **ForgotPasswordView:** email field + send reset button + success state
- **AuthInteractor:** all API call logic (pluggable — buyer swaps endpoint URL). Token saved to Keychain on success.
- **AuthPresenter:** all validation logic (email format, password min 8 chars, confirm password match)
- Flow: success → save token to Keychain → navigate to TabBar. Error → show inline error state.
- Custom auth (no vendor lock-in): buyer can plug any backend (Firebase, Supabase, custom REST, etc.)

### TabBar
- 4 tabs: Home, Explore (placeholder), Profile (placeholder), Settings
- SF Symbols icons with badge support ready
- iPad: automatic sidebar navigation via `NavigationSplitView` when width is sufficient

### Home
- Sample list view with pull-to-refresh
- Loading state → data → empty state (depending on API response)
- Demonstrates full networking flow end-to-end: fetch → decode → display
- Mock data for previews and first run

### Settings
- **Profile section:** avatar, name, email (read-only display)
- **Preferences section:** notifications toggle, theme picker (dark/light/system), language selector
- **About section:** app version, terms of service, privacy policy (placeholder URLs)
- **Logout button:** clear Keychain token → navigate to Auth
- Theme picker applies immediately via `ThemeManager` using `@AppStorage`

---

## Core Infrastructure

### Network Layer (`Core/Network/`)
- `APIClient` — generic async/await HTTP client (URLSession)
- Auto-attach auth token from Keychain to `Authorization: Bearer <token>` header
- JSON encoding/decoding via `Codable`
- `APIError` enum: `.unauthorized`, `.notFound`, `.serverError`, `.noConnection`, `.decodingError`, `.custom(String)`
- `APIEndpoint` protocol: `path`, `method`, `headers`, `body`, `queryItems` — buyer defines new endpoints by conforming
- `MockAPIClient` — returns dummy data for SwiftUI Previews and testing without a server
- All responses wrapped in `Result<T, APIError>` at Interactor level

### Storage (`Core/Storage/`)
- `KeychainManager` — save/read/delete tokens and credentials (Security framework wrapper, no third-party)
- `UserDefaultsManager` — app preferences (theme, language, hasSeenOnboarding, notification settings)
- `StorageKeys` enum — centralized key constants, no magic strings

### Theme (`Core/Theme/`)
- `ThemeManager` — `ObservableObject` with `@AppStorage`, toggles dark/light/system
- `AppTheme` struct — centralized colors, fonts, spacing, corner radius. Buyer edits 1 file = entire app updates.
- `AppColors` — semantic color names (primary, secondary, background, surface, error, textPrimary, textSecondary) that auto-adapt to dark mode via Color Assets

### Localization (`Core/Localization/`)
- English (default) + Bahasa Indonesia
- All UI strings in `Strings.swift` referencing `Localizable.strings`
- Buyer adds new language by creating a new `.lproj` folder

### Push Notifications
- `AppDelegate` — register for remote notifications, handle device token
- Device token sent to API via `APIClient` (placeholder endpoint)
- `NotificationManager` — request permission, handle foreground notification display via `UNUserNotificationCenterDelegate`
- Buyer plugs their server-side push provider (FCM, OneSignal, custom APN)

---

## SharedUI Components

| Component | Description |
|-----------|-------------|
| `LoadingView` | Spinner + optional message text |
| `EmptyStateView` | Illustration + title + subtitle + action button |
| `ErrorStateView` | Error icon + message + retry button |
| `PrimaryButton` | Styled button with loading state (spinner replaces label) |
| `InputField` | Text field with label, validation error message, secure toggle for passwords |
| `AvatarView` | Circle image with placeholder initials fallback |

All components support dark mode and iPad adaptive sizing.

---

## VIPER Convention Rules

- **1 type per file** — no multiple structs/classes in one file
- **Max 200 lines per file** — split if exceeding
- **No magic strings** — all in `Constants/` or `StorageKeys`
- **No hardcoded colors** — all via `AppTheme` / `AppColors`
- **Router** — handles navigation (creating views, pushing, presenting)
- **Interactor** — business logic + API calls
- **Presenter** — transforms data for View, handles validation
- **View** — pure SwiftUI, only displays what Presenter provides
- **Entity** — data models (Codable structs)

---

## Deliverables

### ZIP contents:
```
SwiftUIStarterKit-v1.0.zip
├── SwiftUIStarterKit/           # Full Xcode project — open, build, run
├── README.md                    # Quick start (3 steps), screenshots, feature list
├── CUSTOMIZATION.md             # Rename app, swap API, add module, change theme, add language
├── ARCHITECTURE.md              # VIPER explanation + diagram, file naming convention
└── SCREENSHOTS/                 # 4-5 preview images (onboarding, login, home, settings, dark mode)
```

### README.md:
- "Open → Build → Run" in 3 steps
- Feature checklist
- Screenshot grid
- Requirements: Xcode 16+, iOS 17+, Swift 5.9+

### CUSTOMIZATION.md:
- How to rename the app (bundle ID, display name)
- How to change theme colors (edit `AppTheme.swift`)
- How to add a new VIPER module (copy 5-file template)
- How to connect real API (set base URL in `AppConstants.swift`, define endpoints)
- How to add a new language (create `.lproj`, add translations)
- How to remove modules you don't need

### ARCHITECTURE.md:
- VIPER pattern explanation with data flow diagram
- File naming convention
- Module communication rules
- When to use Router vs Presenter vs Interactor

---

## Gumroad Listing

- **Title:** SwiftUI Starter Kit — VIPER Boilerplate for iOS & iPad
- **Price:** $29
- **Tags:** SwiftUI, iOS, iPad, boilerplate, template, VIPER, starter kit, Xcode
- **Cover:** Screenshot collage (onboarding + login + home + settings + dark mode)
- **Description highlights:**
  - Zero dependencies — pure Apple frameworks
  - VIPER architecture — scalable & testable
  - Universal (iPhone + iPad adaptive)
  - Dark mode + localization (EN/ID) included
  - Custom auth flow — plug any backend
  - 10 features ready out of the box
  - 3 detailed docs (README, CUSTOMIZATION, ARCHITECTURE)
