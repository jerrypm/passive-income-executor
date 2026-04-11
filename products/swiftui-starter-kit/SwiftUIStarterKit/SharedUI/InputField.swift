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
