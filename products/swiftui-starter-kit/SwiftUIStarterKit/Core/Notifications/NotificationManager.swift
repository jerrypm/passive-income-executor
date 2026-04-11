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
