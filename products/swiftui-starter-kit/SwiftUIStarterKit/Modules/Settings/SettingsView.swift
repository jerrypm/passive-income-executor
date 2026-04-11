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
