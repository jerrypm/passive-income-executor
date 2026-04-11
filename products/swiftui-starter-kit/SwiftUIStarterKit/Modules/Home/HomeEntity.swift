import Foundation

struct HomeItem: Codable, Identifiable {
    let id: String
    let title: String
    let subtitle: String
}

enum HomeEndpoint: APIEndpoint {
    case fetchItems

    var path: String { "/items" }
    var method: HTTPMethod { .get }
}
