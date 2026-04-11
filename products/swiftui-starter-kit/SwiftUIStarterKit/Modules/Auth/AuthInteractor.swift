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
