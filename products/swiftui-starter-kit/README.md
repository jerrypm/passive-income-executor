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
