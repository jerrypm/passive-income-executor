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
