import Foundation

enum APIError: LocalizedError {
    case unauthorized
    case notFound
    case serverError(Int)
    case noConnection
    case decodingError
    case custom(String)

    var errorDescription: String? {
        switch self {
        case .unauthorized: "Unauthorized"
        case .notFound: "Resource not found"
        case .serverError(let code): "Server error (\(code))"
        case .noConnection: "No internet connection"
        case .decodingError: "Failed to decode response"
        case .custom(let msg): msg
        }
    }
}
