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
