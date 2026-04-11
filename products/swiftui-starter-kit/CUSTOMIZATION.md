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
