import Foundation

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case delete = "DELETE"
}

protocol APIEndpoint {
    var path: String { get }
    var method: HTTPMethod { get }
    var body: Data? { get }
    var queryItems: [URLQueryItem]? { get }
}

extension APIEndpoint {
    var body: Data? { nil }
    var queryItems: [URLQueryItem]? { nil }

    var url: URL? {
        var components = URLComponents(string: AppConstants.apiBaseURL + path)
        components?.queryItems = queryItems
        return components?.url
    }
}
