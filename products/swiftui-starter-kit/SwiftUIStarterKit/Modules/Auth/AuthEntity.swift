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
